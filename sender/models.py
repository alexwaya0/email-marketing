# sender/models.py
from django.db import models

class UserEmail(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} - {self.email}"

class EmailTemplate(models.Model):
    name = models.CharField(max_length=255, default="Default Template")
    html_content = models.TextField()

    def __str__(self):
        return self.name