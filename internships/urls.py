from django.urls import path
from . import views

urlpatterns = [
    path('open_internindex', views.open_internindex, name="open_internindex"),
    path(
        "",
        views.internship_index,
        name="internship_index"
    ),
     path(
        'add_internship/', views.add_internship, name='add_internship'
    ),
     
     path(
        "details/<int:id>/",
        views.internship_details,
        name="internship_detail"
    ),
     path(
         "admin/<int:id>/edit/",
         views.edit_internship,
         name="admin_edit_internship",
     ),
     path(
         "admin/<int:id>/delete/",
         views.delete_internship,
         name="admin_delete_internship",
     ),
]
