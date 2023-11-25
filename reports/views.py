from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pets.models import *
from donation.models import *
from django.db.models import DecimalField, F, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone



# Create your views here.
def render_pdf_view(request):
    template_path = 'reports/pet.html'
    context = {'myvar': 'this is your template context'}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    response['Content-Disposition'] = 'filename="report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="application_form.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

from django.shortcuts import get_object_or_404

def application_form_pdf(request, application_id):
    application = get_object_or_404(Application, applicationId=application_id)
    interviews = Interview.objects.filter(application=application)
    
    try:
        turnover = Turnover.objects.get(application=application)
    except Turnover.DoesNotExist:
        turnover = None  # Handle the case where Turnover does not exist
    
    house_pictures = HousePicture.objects.filter(applicationId=application)
    id_pictures = IdPicture.objects.filter(applicationId=application)
    
    try:
        condo_agreement = CondoAgreement.objects.get(applicationId=application)
    except CondoAgreement.DoesNotExist:
        condo_agreement = None  # Handle the case where CondoAgreement does not exist

    context = {
        'application': application,
        'interviews': interviews,
        'turnover': turnover,
        'house_pictures': house_pictures,
        'id_pictures': id_pictures,
        'condo_agreement': condo_agreement,
    }

    return render_to_pdf('reports/application_form.html', context)

def pet_render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="all_pets_information.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def all_pets_information_pdf(request):
    all_pets = Pet.objects.all()

    pets_info = []
    for pet in all_pets:
        pet_images = PetImage.objects.filter(petId=pet)
        
        try:
            pet_medical = PetMedical.objects.get(petId=pet)
        except PetMedical.DoesNotExist:
            pet_medical = None  # Handle the case where PetMedical does not exist
        
        pets_info.append({
            'pet': pet,
            'pet_images': pet_images,
            'pet_medical': pet_medical,
        })

    context = {
        'pets_info': pets_info,
    }

    return pet_render_to_pdf('reports/pet.html', context)


def donation_render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="donation_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

from django.db.models import Sum
from django.db.models.functions import Coalesce

def generate_donation_pdf(request, campaign_id):
    campaign = FundraisingCampaign.objects.get(campaignId=campaign_id)
    donations = Donation.objects.filter(campaign=campaign)
    payments = Payment.objects.filter(donation__in=donations)

    # Calculate total amount donated
    total_donated = Donation.objects.filter(campaign=campaign).aggregate(Sum('donationAmount'))['donationAmount__sum']
    total_donated_float = float(total_donated)
    # Calculate the percentage of the goal to the total amount donated
    percentage_goal_to_total = (total_donated_float / float(campaign.campaignGoal)) * 100 if campaign.campaignGoal > 0 else 0
    current_datetime = timezone.now()
    context = {
        'campaign': campaign,
        'donations': donations,
        'payments': payments,
        'percentage_goal_to_total': percentage_goal_to_total,
        'total_donated': total_donated,
        'current_datetime': current_datetime,
    }

    pdf = donation_render_to_pdf('reports/donation.html', context)
    return HttpResponse(pdf, content_type='application/pdf')