from django.urls import path
from . import views

urlpatterns = [
    path('open_signup', views.open_signup, name="open_signup"),
    path('open_login', views.open_login, name="open_login"),
    path('open_industrylogin', views.open_industrylogin, name='open_industrylogin'),
    path('open_industrysignup', views.open_industrysignup, name='open_industrysignup'),
    path('open_adminlogin', views.open_adminlogin, name="open_adminlogin"),
    path("logout/", views.account_logout, name="account_logout"),
    path(
        "admin/students/<int:student_id>/delete/",
        views.delete_student,
        name="admin_delete_student",
    ),
    path(
        "admin/industries/<int:industry_id>/delete/",
        views.delete_industry,
        name="admin_delete_industry",
    ),
    path(
        "industry/applications/<int:application_id>/resume/",
        views.download_applicant_resume,
        name="download_applicant_resume",
    ),
     path("student_dashboard/",views.student_dashboard,name="student_dashboard" ),
     path("student/profile/", views.student_profile, name="student_profile"),
     path("industry_dashboard", views.industry_dashboard, name="industry_dashboard"),
    path("admin_dashboard", views.admin_dashboard, name="admin_dashboard"),
]
