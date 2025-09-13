from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
import pandas as pd

from .models import UserEmail, EmailTemplate
from .forms import UploadExcelForm, EmailTemplateForm


def dashboard(request):
    emails = UserEmail.objects.all()
    last_upload = UserEmail.objects.order_by('-id').first()
    return render(request, 'sender/dashboard.html', {
        'emails': emails,
        'last_upload': last_upload
    })


def upload_excel(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            for _, row in df.iterrows():
                username = row['username']
                email = row['email']
                if not UserEmail.objects.filter(email=email).exists():
                    UserEmail.objects.create(username=username, email=email)
            messages.success(request, "Excel file uploaded and emails saved.")
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
    messages.success(request, f"Email {email.email} deleted successfully.")
    return redirect('email_list')


def send_emails(request):
    template = EmailTemplate.objects.first()
    if not template:
        messages.error(request, "No email template found. Please create one before sending emails.")
        return redirect('edit_template')

    emails = UserEmail.objects.all()
    if not emails.exists():
        messages.warning(request, "No recipients found in the system.")
        return redirect('email_list')

    # Pagination setup for batching
    paginator = Paginator(emails, 50)  # 👈 send 50 per batch
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    for user_email in page_obj.object_list:
        context = {'username': user_email.username}
        html_content = render_to_string('sender/email_template.html', context)
        text_content = strip_tags(html_content)

        # This will print to console instead of sending
        msg = EmailMultiAlternatives(
            subject="Hello from Django App",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()  # with console backend → prints in terminal

    # If there’s another page, redirect to it
    if page_obj.has_next():
        next_url = f"{request.path}?page={page_obj.next_page_number()}"
        messages.info(request, f"Batch {page_number} processed. Continuing to next batch...")
        return redirect(next_url)

    messages.success(request, "All emails processed successfully! (Check your terminal output).")
    return redirect('email_list')


def edit_template(request):
    template, created = EmailTemplate.objects.get_or_create(name="Default Template")
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, "Template updated successfully.")
            return redirect('dashboard')
    else:
        form = EmailTemplateForm(instance=template)
    return render(request, 'sender/edit_template.html', {'form': form})
