from django.urls import path
from . import views

urlpatterns = [
    path('campaign/<str:campaign_id>/', views.campaign_details, name='campaign_details'),
    path('donation_page/', views.donation_page, name='donation_page'),
    path('donate/<str:campaign_id>/', views.donate, name='donate'),

]