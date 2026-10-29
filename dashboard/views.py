from django.shortcuts import redirect, render

# Create your views here.
def open_studentdashboard(request):
    return render(request, "dashboard/student_dashboard.html")

def open_industrydashboard(request):
    return redirect("industry_dashboard")

def open_admindashboard(request):
    return redirect("admin_dashboard")
