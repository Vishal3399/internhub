from django.test import TestCase
from django.urls import reverse

from .models import Internship


class InternshipSearchPageTests(TestCase):
    def setUp(self):
        self.internship = Internship.objects.create(
            company="Example Tech",
            title="Backend Developer Intern",
            location="Bengaluru",
            work_mode="Remote",
            duration="3 months",
            stipend="Paid",
            skills="Python, Django",
            about="Build backend services.",
            responsibilities="Work with the engineering team.",
            requirements="Basic Python experience.",
            last_date="2027-01-01",
        )

    def test_search_and_skill_filter_controls_render(self):
        response = self.client.get(reverse("internship_index"))

        self.assertContains(response, 'id="search-query"')
        self.assertContains(response, 'id="location-query"')
        self.assertContains(response, 'name="mode"')
        for skill in ("python", "java", "django", "php"):
            self.assertContains(response, f'name="skill" value="{skill}"')

    def test_internship_listing_exposes_searchable_skills(self):
        response = self.client.get(reverse("internship_index"))

        self.assertContains(response, 'data-skills="python, django"')
        self.assertContains(response, "Backend Developer Intern")
