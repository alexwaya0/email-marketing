# sender/forms.py
from django import forms
from .models import EmailTemplate, UserEmail

class UploadExcelForm(forms.Form):
    excel_file = forms.FileField()

class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['html_content']
        widgets = {
            'html_content': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }

class AddEmailForm(forms.ModelForm):
    class Meta:
        model = UserEmail
        fields = ['username', 'email']