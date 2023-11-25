from django.urls import path
from .views import *

app_name = 'pets'

urlpatterns = [
    path('render', render_pdf_view, name='test-view'),
    path('pdf/application_form/<str:application_id>/', application_form_pdf, name='application_form_pdf'),
    path('pdf/all_pets_information/', all_pets_information_pdf, name='all_pets_information_pdf'),
    path('pdf/generate-donation-pdf/<str:campaign_id>/', generate_donation_pdf, name='generate_donation_pdf'),
]