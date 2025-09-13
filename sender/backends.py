from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.conf import settings
from .models import SiteSettings


class DynamicSMTPBackend(SMTPBackend):
    def __init__(self, *args, **kwargs):
        try:
            site_settings = SiteSettings.objects.get()
            host = site_settings.email_host or getattr(settings, 'EMAIL_HOST', 'smtp.gmail.com')
            port = site_settings.email_port or getattr(settings, 'EMAIL_PORT', 587)
            username = site_settings.email_host_user or getattr(settings, 'EMAIL_HOST_USER', '')
            password = site_settings.email_host_password or getattr(settings, 'EMAIL_HOST_PASSWORD', '')
            use_tls = site_settings.email_use_tls if site_settings.email_use_tls is not None else getattr(settings, 'EMAIL_USE_TLS', True)
            use_ssl = site_settings.email_use_ssl if site_settings.email_use_ssl is not None else getattr(settings, 'EMAIL_USE_SSL', False)
            default_from_email = site_settings.default_from_email or getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
        except SiteSettings.DoesNotExist:
            host = getattr(settings, 'EMAIL_HOST', 'smtp.gmail.com')
            port = getattr(settings, 'EMAIL_PORT', 587)
            username = getattr(settings, 'EMAIL_HOST_USER', '')
            password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
            use_tls = getattr(settings, 'EMAIL_USE_TLS', True)
            use_ssl = getattr(settings, 'EMAIL_USE_SSL', False)
            default_from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')

        super().__init__(
            host=host,
            port=port,
            username=username,
            password=password,
            use_tls=use_tls,
            use_ssl=use_ssl,
            *args,
            **kwargs
        )
        self.default_from_email = default_from_email

    def send_messages(self, email_messages):
        for message in email_messages:
            if message.from_email is None:
                message.from_email = self.default_from_email
        return super().send_messages(email_messages)