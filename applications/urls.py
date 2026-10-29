from django.urls import path

from . import views

urlpatterns = [
    path(
        "internships/<int:internship_id>/apply/",
        views.apply_to_internship,
        name="apply_to_internship",
    ),
]
