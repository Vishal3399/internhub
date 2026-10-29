from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import Student
from applications.models import Application
from .forms import InternshipForm
from .models import Internship

# Create your views here.
def open_internindex(request):
    return render(request, "internships/internship_index.html")


def internship_index(request):
    internships = Internship.objects.all().order_by("-created_at")
    student_id = request.session.get("student_id")
    is_student = (
        request.session.get("account_type") == "student"
        and Student.objects.filter(id=student_id).exists()
    )

    return render(
        request,
        "internships/internship_index.html",
        {
            "internships": internships,
            "is_student": is_student,
            "applied_internship_ids": (
                Application.objects.filter(student_id=student_id).values_list(
                    "internship_id", flat=True
                )
                if is_student
                else ()
            ),
        }
    )


def add_internship(request):

    if request.method == "POST":
        form = InternshipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("internship_index")
    else:
        form = InternshipForm()

    return render(
        request,
        "internships/add_internship.html",
        {"form": form},
    )
    
    


def internship_details(request, id):
    internship = get_object_or_404(Internship, id=id)
    student_id = request.session.get("student_id")
    is_student = (
        request.session.get("account_type") == "student"
        and Student.objects.filter(id=student_id).exists()
    )

    return render(
        request,
        "internships/internship_details.html",
        {
            "internship": internship,
            "is_student": is_student,
            "has_applied": (
                Application.objects.filter(
                    student_id=student_id,
                    internship=internship,
                ).exists()
                if is_student
                else False
            ),
        }
    )


def _is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(_is_admin, login_url="open_adminlogin")
def edit_internship(request, id):
    internship = get_object_or_404(Internship, id=id)
    form = InternshipForm(request.POST or None, instance=internship)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("admin_dashboard")

    return render(
        request,
        "internships/edit_internship.html",
        {"form": form, "internship": internship},
    )


@require_POST
@user_passes_test(_is_admin, login_url="open_adminlogin")
def delete_internship(request, id):
    internship = get_object_or_404(Internship, id=id)
    internship.delete()
    return redirect("admin_dashboard")
