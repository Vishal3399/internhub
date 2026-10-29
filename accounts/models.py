from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):

    full_name = models.CharField(max_length=150)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    college = models.CharField(max_length=200)

    course = models.CharField(max_length=100)

    graduation_year = models.IntegerField()

    skills = models.CharField(max_length=500, blank=True)

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    password = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
    
    
class Industry(models.Model):
    company_name = models.CharField(max_length=150)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    company_website = models.URLField(max_length=300, blank=True)
    industry_type = models.CharField(max_length=120)
    location = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return self.company_name
    
    