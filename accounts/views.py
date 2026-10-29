from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST

from .models import Industry, Student
from internships.models import Internship
from applications.models import Application
from .forms import StudentProfileForm

# Create your views here.

#Student Signup views
def open_signup(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        college = request.POST.get("college")
        course = request.POST.get("course")
        graduation_year = request.POST.get("graduation_year")
        skills = request.POST.get("skills")
        resume = request.FILES.get("resume")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check password
        if password != confirm_password:
            return render(
                request,
                "accounts/student_signup.html",
                {
                    "error": "Passwords do not match."
                }
            )

        # Check email already exists
        if Student.objects.filter(email=email).exists():
            return render(
                request,
                "accounts/student_signup.html",
                {
                    "error": "Email already registered."
                }
            )

        # Save student
        Student.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            college=college,
            course=course,
            graduation_year=graduation_year,
            skills=skills,
            resume=resume,
            password=password
        )

        return redirect("open_login")

    return render(
        request,
        "accounts/student_signup.html"
    )

#Student login views
def open_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            student = Student.objects.get(email=email, password=password)
            request.session["account_type"] = "student"
            request.session["student_id"] = student.id
            return redirect("student_dashboard")
        
        except Student.DoesNotExist:
            return render(request, "accounts/student_login.html", {"error": "Invalid Email or Password"})
            
    return render(request, 'accounts/student_login.html')

#Student dashboard views
def student_dashboard(request):
    if request.session.get("account_type") != "student":
        return redirect("open_login")

    student = Student.objects.filter(
        id=request.session.get("student_id")
    ).first()
    if student is None:
        request.session.pop("account_type", None)
        request.session.pop("student_id", None)
        return redirect("open_login")

    applications = Application.objects.filter(student=student).select_related(
        "internship"
    )
    return render(
        request,
        "dashboard/student_dashboard.html",
        {
            "student": student,
            "applications": applications,
        },
    )


def student_profile(request):
    if request.session.get("account_type") != "student":
        return redirect("open_login")

    student = Student.objects.filter(
        id=request.session.get("student_id")
    ).first()
    if student is None:
        request.session.pop("account_type", None)
        request.session.pop("student_id", None)
        return redirect("open_login")

    form = StudentProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=student,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("student_dashboard")

    return render(
        request,
        "accounts/student_profile.html",
        {"form": form, "student": student},
    )




def open_industrysignup(request):
    if request.method == "POST":
            company_name = request.POST.get("company_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            phone_number = request.POST.get("phone_number")
            company_website = request.POST.get("company_website")
            industry_type = request.POST.get("industry_type")
            location = request.POST.get("location")
            description = request.POST.get("description")
            
            if password != confirm_password:
                return render(
                    request,
                    "accounts/industry_signup.html",
                    {"error": "Password do not match"}
                )
                
            if Industry.objects.filter(email=email).exists():
                return render(
                    request,
                    "accounts/industry_signup.html",
                    {"error": "Email already exists"}
                )
                
            Industry.objects.create(
                company_name=company_name,
                email=email,
                password=password,
                phone_number=phone_number,
                company_website=company_website,
                industry_type=industry_type,
                location=location,
                description=description
            )
            
            return redirect("open_industrylogin")
        
    return render(request, "accounts/industry_signup.html")



def open_industrylogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            industry = Industry.objects.get(email=email, password=password)
            request.session["account_type"] = "industry"
            request.session["industry_id"] = industry.id
            request.session.pop("student_id", None)
            return redirect("industry_dashboard")
        
        except Industry.DoesNotExist:
            return render(
                request,
                "accounts/industry_login.html",
                {"error": "Invalid email or password."}
            )
        
    return render(request, "accounts/industry_login.html")


def industry_dashboard(request):
    if request.session.get("account_type") != "industry":
        return redirect("open_industrylogin")

    industry = Industry.objects.filter(
        id=request.session.get("industry_id")
    ).first()
    if industry is None:
        request.session.pop("account_type", None)
        request.session.pop("industry_id", None)
        return redirect("open_industrylogin")

    internships = Internship.objects.filter(
        company=industry.company_name
    ).order_by("-created_at")
    applications = (
        Application.objects.filter(internship__in=internships)
        .select_related("student", "internship")
        .order_by("-applied_at")
    )
    return render(
        request,
        "dashboard/industry_dashboard.html",
        {
            "industry": industry,
            "internships": internships,
            "applications": applications,
            "application_count": applications.count(),
        },
    )



def open_adminlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(
            request,
            username=username,
            password=password
        )
        
        if user is not None and user.is_superuser:
            login(request, user)
            request.session["account_type"] = "admin"
            request.session.pop("student_id", None)
            return redirect("admin_dashboard")

        return render(
            request,
            "accounts/admin_login.html",
            {"error": "Invalid admin username or password"}
        )
            
    return render(request, "accounts/admin_login.html")

def _is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(_is_admin, login_url="open_adminlogin")
def admin_dashboard(request):
    return render(
        request,
        "dashboard/admin_dashboard.html",
        {
            "internships": Internship.objects.order_by("-created_at"),
            "industries": Industry.objects.order_by("-created_at"),
            "students": Student.objects.order_by("-created_at"),
        },
    )


@require_POST
@user_passes_test(_is_admin, login_url="open_adminlogin")
def delete_student(request, student_id):
    student = Student.objects.filter(id=student_id).first()
    if student is not None:
        student.delete()
    return redirect("admin_dashboard")


@require_POST
@user_passes_test(_is_admin, login_url="open_adminlogin")
def delete_industry(request, industry_id):
    industry = Industry.objects.filter(id=industry_id).first()
    if industry is not None:
        Internship.objects.filter(company=industry.company_name).delete()
        industry.delete()
    return redirect("admin_dashboard")


def download_applicant_resume(request, application_id):
    if request.session.get("account_type") != "industry":
        return redirect("open_industrylogin")

    industry = Industry.objects.filter(
        id=request.session.get("industry_id")
    ).first()
    if industry is None:
        request.session.pop("account_type", None)
        request.session.pop("industry_id", None)
        return redirect("open_industrylogin")

    application = Application.objects.filter(
        id=application_id,
        internship__company=industry.company_name,
    ).select_related("student", "internship").first()
    if application is None or not application.student.resume:
        raise Http404("Resume not found.")

    resume = application.student.resume
    try:
        file_handle = resume.open("rb")
    except (OSError, ValueError) as error:
        raise Http404("Resume not found.") from error

    return FileResponse(
        file_handle,
        as_attachment=True,
        filename=resume.name.rsplit("/", 1)[-1],
    )


def account_logout(request):
    request.session.flush()
    return redirect("index")