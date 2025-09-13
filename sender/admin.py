from django.contrib import admin
from .models import UserEmail, EmailTemplate, SiteSettings


@admin.register(UserEmail)
class UserEmailAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    search_fields = ("username", "email")
    ordering = ("username",)


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    # Make editing easier for long HTML templates
    fieldsets = (
        (None, {
            "fields": ("name", "html_content"),
            "description": "Define reusable email templates with HTML content."
        }),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("email_backend", "email_host", "email_port", "default_from_email")
    search_fields = ("email_backend", "email_host", "email_host_user", "default_from_email")
    fieldsets = (
        ("Backend", {
            "fields": ("email_backend",),
            "description": "Select the Django email backend to use."
        }),
        ("SMTP Settings", {
            "fields": ("email_host", "email_port", "email_use_tls", "email_use_ssl"),
            "description": "Configure your SMTP server details."
        }),
        ("Authentication", {
            "fields": ("email_host_user", "email_host_password"),
            "description": "Provide login details for your SMTP server."
        }),
        ("Default Email", {
            "fields": ("default_from_email",),
            "description": "Set the default email sender address."
        }),
    )

    def has_add_permission(self, request):
        """
        Prevent multiple SiteSettings objects. Only one should exist.
        """
        return not SiteSettings.objects.exists()


