from django.contrib import admin
from django.http import HttpResponse
from .models import UserEmail, EmailTemplate, SiteSettings
import openpyxl
from datetime import datetime


@admin.register(UserEmail)
class UserEmailAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    search_fields = ("username", "email")
    ordering = ("username",)
    actions = ["export_to_excel"]

    def export_to_excel(self, request, queryset):
        """
        Export selected UserEmail objects to an Excel file.
        """
        # Create a new workbook and select the active sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "User Emails"

        # Define headers
        headers = ["Username", "Email"]
        sheet.append(headers)

        # Add data from queryset
        for user in queryset:
            sheet.append([user.username, user.email])

        # Prepare response with Excel file
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        response["Content-Disposition"] = f"attachment; filename=user_emails_{timestamp}.xlsx"

        # Save workbook to response
        workbook.save(response)
        return response

    export_to_excel.short_description = "Export selected users to Excel"


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