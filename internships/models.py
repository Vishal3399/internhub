from django.db import models

# Create your models here.
class Internship(models.Model):
    company = models.CharField(max_length=150)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=150)

    work_mode = models.CharField(max_length=50)

    duration = models.CharField(max_length=100)
    stipend = models.CharField(max_length=100)

    skills = models.TextField()

    about = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()

    last_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company}"