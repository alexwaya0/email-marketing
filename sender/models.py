from django.db import models


class UserEmail(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} <{self.email}>"

    class Meta:
        verbose_name = "User Email"
        verbose_name_plural = "User Emails"


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    html_content = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Email Template"
        verbose_name_plural = "Email Templates"


class SiteSettings(models.Model):
    email_backend = models.CharField(
        max_length=255,
        default='django.core.mail.backends.smtp.EmailBackend',
        help_text="Email backend (e.g., 'django.core.mail.backends.smtp.EmailBackend' for SMTP)."
    )
    email_host = models.CharField(
        max_length=255,
        blank=True,
        help_text="SMTP server host (e.g., 'smtp.gmail.com')."
    )
    email_port = models.PositiveIntegerField(
        default=587,
        help_text="SMTP server port (e.g., 587 for TLS, 465 for SSL)."
    )
    email_use_tls = models.BooleanField(
        default=True,
        help_text="Use TLS for secure connection (recommended for port 587)."
    )
    email_use_ssl = models.BooleanField(
        default=False,
        help_text="Use SSL for secure connection (enable for port 465, disable for TLS)."
    )
    email_host_user = models.CharField(
        max_length=255,
        blank=True,
        help_text="SMTP server username (e.g., your email address)."
    )
    email_host_password = models.CharField(
        max_length=255,
        blank=True,
        help_text="SMTP server password or app-specific password."
    )
    default_from_email = models.EmailField(
        blank=True,
        help_text="Default sender email address (e.g., 'your-email@example.com')."
    )

    def __str__(self):
        return "Site Email Settings"

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"