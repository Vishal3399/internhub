import tempfile

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from accounts.models import Industry, Student
from applications.models import Application
from internships.models import Internship


class StudentInternshipSessionTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            full_name="Test Student",
            email="student@example.com",
            phone="1234567890",
            college="Test University",
            course="Computer Science",
            graduation_year=2027,
            skills="Python",
            password="test-password",
        )
        self.internship = Internship.objects.create(
            company="Example Company",
            title="Software Intern",
            location="Remote",
            work_mode="Remote",
            duration="3 months",
            stipend="Paid",
            skills="Python",
            about="Build useful software.",
            responsibilities="Work with the engineering team.",
            requirements="Basic Python experience.",
            last_date="2027-01-01",
        )

    def test_student_session_is_recognized_on_internship_details(self):
        login_response = self.client.post(
            reverse("open_login"),
            {"email": self.student.email, "password": "test-password"},
        )

        self.assertRedirects(login_response, reverse("student_dashboard"))
        self.assertEqual(self.client.session["account_type"], "student")
        self.assertContains(
            self.client.get(reverse("internship_index")),
            "Student dashboard",
        )
        self.assertContains(
            self.client.get(reverse("internship_index")),
            "Apply",
        )

        detail_response = self.client.get(
            reverse("internship_detail", args=[self.internship.id])
        )

        self.assertContains(detail_response, 'type="submit">Apply</button>')
        self.assertNotContains(detail_response, "Sign in to continue")

    def test_signed_out_visitor_is_prompted_to_sign_in(self):
        detail_response = self.client.get(
            reverse("internship_detail", args=[self.internship.id])
        )
        listing_response = self.client.get(reverse("internship_index"))

        self.assertContains(detail_response, "Sign in to apply")
        self.assertContains(listing_response, "Sign in to apply")

    def test_student_logout_clears_student_session(self):
        self.client.post(
            reverse("open_login"),
            {"email": self.student.email, "password": "test-password"},
        )

        logout_response = self.client.get(reverse("account_logout"))

        self.assertRedirects(logout_response, reverse("index"))
        self.assertNotIn("account_type", self.client.session)

    def test_student_can_apply_once_and_see_application_on_dashboard(self):
        self.client.post(
            reverse("open_login"),
            {"email": self.student.email, "password": "test-password"},
        )

        apply_url = reverse(
            "apply_to_internship",
            args=[self.internship.id],
        )
        response = self.client.post(apply_url)
        self.assertRedirects(
            response,
            reverse("internship_detail", args=[self.internship.id]),
        )
        self.assertEqual(Application.objects.count(), 1)

        self.client.post(apply_url)
        self.assertEqual(Application.objects.count(), 1)

        detail_response = self.client.get(
            reverse("internship_detail", args=[self.internship.id])
        )
        dashboard_response = self.client.get(reverse("student_dashboard"))
        self.assertContains(detail_response, "Applied")
        self.assertNotContains(detail_response, 'type="submit">Apply</button>')
        self.assertContains(dashboard_response, self.internship.title)
        self.assertContains(dashboard_response, "Applied")

    def test_student_can_update_profile(self):
        self.client.post(
            reverse("open_login"),
            {"email": self.student.email, "password": "test-password"},
        )

        response = self.client.post(
            reverse("student_profile"),
            {
                "full_name": "Updated Student",
                "email": "updated@example.com",
                "phone": "9998887777",
                "college": "Updated University",
                "course": "Software Engineering",
                "graduation_year": "2028",
                "skills": "Python, Django",
            },
        )

        self.assertRedirects(response, reverse("student_dashboard"))
        self.student.refresh_from_db()
        self.assertEqual(self.student.full_name, "Updated Student")
        self.assertEqual(self.student.email, "updated@example.com")

    def test_student_profile_and_dashboard_require_student_session(self):
        profile_response = self.client.get(reverse("student_profile"))
        dashboard_response = self.client.get(reverse("student_dashboard"))

        self.assertRedirects(profile_response, reverse("open_login"))
        self.assertRedirects(dashboard_response, reverse("open_login"))


class AdminManagementTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin-password",
        )
        self.student = Student.objects.create(
            full_name="Admin Test Student",
            email="admin-student@example.com",
            phone="1112223333",
            college="Example College",
            course="Design",
            graduation_year=2028,
            skills="Design",
            password="test-password",
        )
        self.industry = Industry.objects.create(
            company_name="Example Industries",
            email="company@example.com",
            password="test-password",
            phone_number="4445556666",
            industry_type="Technology",
            location="Remote",
            description="An example company.",
        )
        self.internship = Internship.objects.create(
            company="Example Industries",
            title="Product Design Intern",
            location="Remote",
            work_mode="Remote",
            duration="3 months",
            stipend="Paid",
            skills="Design",
            about="Design product experiences.",
            responsibilities="Collaborate with the team.",
            requirements="Design portfolio.",
            last_date="2027-01-01",
        )

    def test_admin_dashboard_shows_management_tables(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("admin_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product Design Intern")
        self.assertContains(response, "Example Industries")
        self.assertContains(response, "Admin Test Student")
        self.assertContains(response, reverse("admin_edit_internship", args=[self.internship.id]))

    def test_admin_can_update_and_delete_internships(self):
        self.client.force_login(self.admin)
        edit_url = reverse("admin_edit_internship", args=[self.internship.id])
        response = self.client.post(
            edit_url,
            {
                "company": "Example Industries",
                "title": "Updated Design Intern",
                "location": "Hybrid",
                "work_mode": "Hybrid",
                "duration": "4 months",
                "stipend": "Paid",
                "skills": "Design, research",
                "about": "Updated role description.",
                "responsibilities": "Updated responsibilities.",
                "requirements": "Updated requirements.",
                "last_date": "2027-02-01",
            },
        )

        self.assertRedirects(response, reverse("admin_dashboard"))
        self.internship.refresh_from_db()
        self.assertEqual(self.internship.title, "Updated Design Intern")

        response = self.client.post(
            reverse("admin_delete_internship", args=[self.internship.id])
        )
        self.assertRedirects(response, reverse("admin_dashboard"))
        self.assertFalse(Internship.objects.filter(id=self.internship.id).exists())

    def test_admin_can_delete_registered_student(self):
        self.client.force_login(self.admin)

        student_response = self.client.post(
            reverse("admin_delete_student", args=[self.student.id])
        )

        self.assertRedirects(student_response, reverse("admin_dashboard"))
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())
        self.assertTrue(Industry.objects.filter(id=self.industry.id).exists())

    def test_admin_can_delete_company_and_its_internship_listings(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("admin_delete_industry", args=[self.industry.id])
        )

        self.assertRedirects(response, reverse("admin_dashboard"))
        self.assertFalse(Industry.objects.filter(id=self.industry.id).exists())
        self.assertFalse(Internship.objects.filter(id=self.internship.id).exists())

    def test_non_admin_cannot_delete_company(self):
        response = self.client.post(
            reverse("admin_delete_industry", args=[self.industry.id])
        )

        self.assertRedirects(
            response,
            f"{reverse('open_adminlogin')}?next={reverse('admin_delete_industry', args=[self.industry.id])}",
        )
        self.assertTrue(Industry.objects.filter(id=self.industry.id).exists())
        self.assertTrue(Internship.objects.filter(id=self.internship.id).exists())

    def test_non_admin_cannot_access_admin_management(self):
        dashboard_response = self.client.get(reverse("admin_dashboard"))
        legacy_dashboard_response = self.client.get(reverse("open_admindashboard"))
        delete_response = self.client.post(
            reverse("admin_delete_student", args=[self.student.id])
        )

        self.assertRedirects(
            dashboard_response,
            f"{reverse('open_adminlogin')}?next={reverse('admin_dashboard')}",
        )
        self.assertRedirects(
            legacy_dashboard_response,
            reverse("admin_dashboard"),
            fetch_redirect_response=False,
        )
        self.assertRedirects(
            delete_response,
            f"{reverse('open_adminlogin')}?next={reverse('admin_delete_student', args=[self.student.id])}",
        )
        self.assertTrue(Student.objects.filter(id=self.student.id).exists())


class IndustryApplicantDashboardTests(TestCase):
    def setUp(self):
        self.industry = Industry.objects.create(
            company_name="Hiring Company",
            email="hiring@example.com",
            password="company-password",
            phone_number="1112223333",
            industry_type="Technology",
            location="Remote",
            description="Hiring company profile.",
        )
        self.other_industry = Industry.objects.create(
            company_name="Other Company",
            email="other@example.com",
            password="company-password",
            phone_number="4445556666",
            industry_type="Design",
            location="Hybrid",
            description="Other company profile.",
        )
        self.internship = Internship.objects.create(
            company=self.industry.company_name,
            title="Backend Intern",
            location="Remote",
            work_mode="Remote",
            duration="3 months",
            stipend="Paid",
            skills="Python",
            about="Build backend features.",
            responsibilities="Work with engineers.",
            requirements="Python experience.",
            last_date="2027-01-01",
        )
        self.other_internship = Internship.objects.create(
            company=self.other_industry.company_name,
            title="Other Company Intern",
            location="Hybrid",
            work_mode="Hybrid",
            duration="3 months",
            stipend="Paid",
            skills="Design",
            about="Support the design team.",
            responsibilities="Design.",
            requirements="Portfolio.",
            last_date="2027-01-01",
        )
        self.applicant = Student.objects.create(
            full_name="Jordan Applicant",
            email="jordan@example.com",
            phone="7778889999",
            college="Example University",
            course="Computer Science",
            graduation_year=2027,
            skills="Python, Django",
            password="student-password",
        )
        self.other_applicant = Student.objects.create(
            full_name="Other Applicant",
            email="other-student@example.com",
            phone="2223334444",
            college="Other University",
            course="Design",
            graduation_year=2028,
            skills="Design",
            password="student-password",
        )
        Application.objects.create(
            student=self.applicant,
            internship=self.internship,
        )
        Application.objects.create(
            student=self.other_applicant,
            internship=self.other_internship,
        )

    def test_industry_dashboard_shows_own_applicants_and_profile_details(self):
        session = self.client.session
        session["account_type"] = "industry"
        session["industry_id"] = self.industry.id
        session.save()

        response = self.client.get(reverse("industry_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jordan Applicant")
        self.assertContains(response, "jordan@example.com")
        self.assertContains(response, "7778889999")
        self.assertContains(response, "Example University")
        self.assertContains(response, "Python, Django")
        self.assertContains(response, "Backend Intern")
        self.assertNotContains(response, "Other Applicant")
        self.assertNotContains(response, "Other Company Intern")

    def test_industry_dashboard_requires_valid_industry_session(self):
        response = self.client.get(reverse("industry_dashboard"))

        self.assertRedirects(response, reverse("open_industrylogin"))

    def test_industry_can_download_resume_for_its_applicant(self):
        application = Application.objects.get(
            student=self.applicant,
            internship=self.internship,
        )
        session = self.client.session
        session["account_type"] = "industry"
        session["industry_id"] = self.industry.id
        session.save()

        with tempfile.TemporaryDirectory() as media_root:
            with self.settings(MEDIA_ROOT=media_root):
                self.applicant.resume.save(
                    "jordan-resume.pdf",
                    ContentFile(b"sample resume data"),
                    save=True,
                )
                response = self.client.get(
                    reverse(
                        "download_applicant_resume",
                        args=[application.id],
                    )
                )

                self.assertEqual(response.status_code, 200)
                self.assertIn(
                    'attachment; filename="jordan-resume.pdf"',
                    response["Content-Disposition"],
                )
                self.assertEqual(
                    b"".join(response.streaming_content),
                    b"sample resume data",
                )
                response.close()

    def test_industry_cannot_download_resume_from_another_company(self):
        other_application = Application.objects.get(
            student=self.other_applicant,
            internship=self.other_internship,
        )
        session = self.client.session
        session["account_type"] = "industry"
        session["industry_id"] = self.industry.id
        session.save()

        response = self.client.get(
            reverse(
                "download_applicant_resume",
                args=[other_application.id],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_resume_download_requires_industry_session(self):
        application = Application.objects.get(
            student=self.applicant,
            internship=self.internship,
        )

        response = self.client.get(
            reverse(
                "download_applicant_resume",
                args=[application.id],
            )
        )

        self.assertRedirects(response, reverse("open_industrylogin"))
