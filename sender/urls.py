from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('emails/', views.EmailListView.as_view(), name='email_list'),
    path('emails/delete/<int:pk>/', views.delete_email, name='delete_email'),
    path('emails/bulk_delete/', views.bulk_delete, name='bulk_delete'),
    path('emails/add/', views.add_email, name='add_email'),
    path('emails/send/', views.send_emails, name='send_emails'),
    path('emails/send_selected/', views.send_selected, name='send_selected'),
    path('template/edit/', views.edit_template, name='edit_template'),
    path('ajax_search/', views.ajax_search, name='ajax_search'),
    path('settings/', views.site_settings, name='site_settings'),
]