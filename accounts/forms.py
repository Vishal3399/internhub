from django import forms

from .models import Student


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            "full_name",
            "email",
            "phone",
            "college",
            "course",
            "graduation_year",
            "skills",
            "resume",
        )
