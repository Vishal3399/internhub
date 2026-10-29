from django.urls import path
from . import views

urlpatterns = [
    path("open_studentdashboard", views.open_studentdashboard, name="open_studentdashboard"),
    path('open_industrydashboard', views.open_industrydashboard, name="open_industrydashboard"),
    path('open_admindashboard', views.open_admindashboard, name="open_admindashboard"),
]
