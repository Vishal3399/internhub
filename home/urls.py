from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('open_index', views.open_index, name="open_index"),
    path('open_loginforms', views.open_loginforms, name="open_loginforms"),
    path('open_aboutus', views.open_aboutus, name="open_aboutus"),
]
