from django import forms
from .models import UserEmail, EmailTemplate, SiteSettings


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(
        label='Upload Excel File',
        help_text='Upload an Excel file containing "username" and "email" columns.',
        widget=forms.FileInput(attrs={'accept': '.xlsx, .xls'})
    )


class AddEmailForm(forms.ModelForm):
    class Meta:
        model = UserEmail
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
        }


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['name', 'html_content']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Template name'}),
            'html_content': forms.Textarea(attrs={'placeholder': 'Enter HTML content here', 'rows': 10}),
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'email_backend',
            'email_host',
            'email_port',
            'email_use_tls',
            'email_use_ssl',
            'email_host_user',
            'email_host_password',
            'default_from_email',
        ]
        widgets = {
            'email_backend': forms.TextInput(attrs={'placeholder': 'e.g., django.core.mail.backends.smtp.EmailBackend'}),
            'email_host': forms.TextInput(attrs={'placeholder': 'e.g., smtp.gmail.com'}),
            'email_port': forms.NumberInput(attrs={'placeholder': 'e.g., 587'}),
            'email_host_user': forms.TextInput(attrs={'placeholder': 'e.g., your-email@example.com'}),
            'email_host_password': forms.PasswordInput(attrs={'placeholder': 'SMTP password or app-specific password'}),
            'default_from_email': forms.EmailInput(attrs={'placeholder': 'e.g., your-email@example.com'}),
        }