from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from accounts.models import Student
from internships.models import Internship

from .models import Application


@require_POST
def apply_to_internship(request, internship_id):
    if request.session.get("account_type") != "student":
        return redirect("open_login")

    student = Student.objects.filter(
        id=request.session.get("student_id")
    ).first()
    if student is None:
        request.session.pop("account_type", None)
        request.session.pop("student_id", None)
        return redirect("open_login")

    internship = get_object_or_404(Internship, id=internship_id)
    _, created = Application.objects.get_or_create(
        student=student,
        internship=internship,
    )
    if created:
        messages.success(request, "Your application has been submitted.")
    else:
        messages.info(request, "You have already applied to this internship.")
    return redirect("internship_detail", id=internship.id)
