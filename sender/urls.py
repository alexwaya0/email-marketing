# sender/urls.py
from django.urls import path
from .views import dashboard, upload_excel, EmailListView, delete_email, send_emails, edit_template, add_email, send_selected, ajax_search, bulk_delete

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('upload/', upload_excel, name='upload_excel'),
    path('emails/', EmailListView.as_view(), name='email_list'),
    path('emails/delete/<int:pk>/', delete_email, name='delete_email'),
    path('send/', send_emails, name='send_emails'),
    path('send_selected/', send_selected, name='send_selected'),
    path('bulk_delete/', bulk_delete, name='bulk_delete'),
    path('template/edit/', edit_template, name='edit_template'),
    path('add/', add_email, name='add_email'),
    path('ajax_search/', ajax_search, name='ajax_search'),
]