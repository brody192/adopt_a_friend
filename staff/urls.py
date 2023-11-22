from django.urls import path
from . import views

urlpatterns = [
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/dashboard/applications/', views.staff_application_dashboard, name='staff_application_dashboard'),
    path('staff/dashboard/campaigns/', views.staff_campaign_dashboard, name='staff_campaign_dashboard'),
    path('staff/dashboard/pets/', views.staff_pet_dashboard, name='staff_pet_dashboard'),
    
    path('staff/dashboard/pets/add_pet/', views.add_pet, name='add_pet'),
    path('staff/dashboard/pets/edit_pet/<slug:slug>/', views.edit_pet, name='edit_pet'),
    path('staff/dashboard/pets/delete_pet/<str:pet_id>/', views.delete_pet, name='delete_pet'),

    # path('staff/dashboard/pets/delete/<slug>/', views.delete_pet, name='delete_pet'),
    
    path('staff/dashboard/campaigns/add_campaign/', views.add_campaign, name='add_campaign'),
    path('staff/dashboard/campaigns/edit_campaign/<str:campaign_id>/', views.edit_campaign, name='edit_campaign'),
    path('staff/dashboard/campaigns/delete_campaign/<str:campaign_id>/', views.delete_campaign, name='delete_campaign'),

    path('staff/dashboard/applications/review/<str:application_id>/', views.review_application, name='review_application'),
    path('generate_application_report/<str:application_id>/', views.generate_application_report, name='generate_application_report'),

    path('generate_pet_data_pdf/', views.generate_pet_data_pdf, name='generate_pet_data_pdf'),

]