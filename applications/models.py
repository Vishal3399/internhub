from django.db import models

from accounts.models import Student
from internships.models import Internship


class Application(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    status = models.CharField(max_length=30, default="Applied")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("student", "internship"),
                name="unique_student_internship_application",
            )
        ]
        ordering = ("-applied_at",)

    def __str__(self):
        return f"{self.student} — {self.internship}"
