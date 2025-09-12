# sender/urls.py
from django.urls import path
from .views import dashboard, upload_excel, EmailListView, delete_email, send_emails, edit_template

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('upload/', upload_excel, name='upload_excel'),
    path('emails/', EmailListView.as_view(), name='email_list'),
    path('emails/delete/<int:pk>/', delete_email, name='delete_email'),
    path('send/', send_emails, name='send_emails'),
    path('template/edit/', edit_template, name='edit_template'),
]