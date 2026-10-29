from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "home/index.html")


def open_index(request):
    return render(request, "home/index.html")

def open_loginforms(request):
    return render(request, "home/loginforms.html")

def open_aboutus(request):
    return render(request, "home/aboutus.html")