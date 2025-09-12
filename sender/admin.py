# sender/admin.py (optional, for admin interface)
from django.contrib import admin
from .models import UserEmail, EmailTemplate

admin.site.register(UserEmail)
admin.site.register(EmailTemplate)