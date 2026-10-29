from django import forms

from .models import Internship


class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = (
            "company",
            "title",
            "location",
            "work_mode",
            "duration",
            "stipend",
            "skills",
            "about",
            "responsibilities",
            "requirements",
            "last_date",
        )
        widgets = {
            "last_date": forms.DateInput(attrs={"type": "date"}),
        }
