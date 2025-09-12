# sender/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import UserEmail, EmailTemplate
from .forms import UploadExcelForm, EmailTemplateForm
import pandas as pd

def dashboard(request):
    return render(request, 'sender/dashboard.html')

def upload_excel(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            # Assume columns: 'username', 'email'
            for _, row in df.iterrows():
                username = row['username']
                email = row['email']
                # Check for duplicates
                if not UserEmail.objects.filter(email=email).exists():
                    UserEmail.objects.create(username=username, email=email)
            return redirect('email_list')
    else:
        form = UploadExcelForm()
    return render(request, 'sender/upload_excel.html', {'form': form})

class EmailListView(ListView):
    model = UserEmail
    template_name = 'sender/email_list.html'
    context_object_name = 'emails'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) | Q(email__icontains=query)
            )
        return queryset

def delete_email(request, pk):
    email = get_object_or_404(UserEmail, pk=pk)
    email.delete()
    return redirect('email_list')

def send_emails(request):
    template = EmailTemplate.objects.first()  # Assume one template for simplicity
    if not template:
        return redirect('edit_template')

    emails = UserEmail.objects.all()
    for user_email in emails:
        context = {'username': user_email.username}
        html_content = render_to_string('sender/email_template.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject="Hello from Django App",
            body=text_content,
            from_email=DEFAULT_FROM_EMAIL,
            to=[user_email.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    return redirect('email_list')

def edit_template(request):
    template, created = EmailTemplate.objects.get_or_create(name="Default Template")
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EmailTemplateForm(instance=template)
    return render(request, 'sender/edit_template.html', {'form': form})