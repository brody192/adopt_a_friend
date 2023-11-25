from django.shortcuts import render, redirect
from .forms import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from pets.models import *
from donation.models import *
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .decorators import staff_required
from reportlab.lib.pagesizes import legal, landscape, letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from PIL import Image
from django.http import FileResponse
import io
from datetime import datetime, timedelta
from django.views.decorators.cache import cache_page

# Create your views here.

@staff_required
def staff_dashboard(request):
    # Retrieve interviewing applications and sort by interviewDate
    interviewing_applications = (
        Application.objects
        .filter(status='Interviewing', interview__isnull=False)
        .order_by('interview__interviewDate')
    )

    unaccessed_threshold = datetime.now() - timedelta(days=7)

    # Retrieve new and unaccessed applications and sort by created_at
    new_and_unaccessed_applications = (
        Application.objects
        .filter(status='Pending', last_accessed_at__lte=unaccessed_threshold)
        .order_by('-created_at')
    )

    # Pass the interviewing applications to the template
    return render(request, 'staff/staff_dashboard.html', {'interviewing_applications': interviewing_applications, 'new_and_unaccessed_applications': new_and_unaccessed_applications})

@staff_required
def staff_application_dashboard(request):
    application = Application.objects.all()
    total_application_count = application.count()
    query = request.GET.get('q')

    if query:
        # Filter campaigns based on the search query
        application = application.filter(
            Q(campaignName__icontains=query) |
            Q(campaignId__icontains=query)
            # Add more fields as needed
            )
    
    return render(request, 'staff/staff_application_dashboard.html', {
        'application':application,
        'total_application_count': total_application_count})

@staff_required
def staff_campaign_dashboard(request):
    fundrasing_campaigns = FundraisingCampaign.objects.all()
    total_campaign_count = fundrasing_campaigns.count()
    query = request.GET.get('q')

    if query:
        # Filter campaigns based on the search query
        fundrasing_campaigns = fundrasing_campaigns.filter(
            Q(campaignName__icontains=query) |
            Q(campaignId__icontains=query)
            # Add more fields as needed
            )

    fundrasing_campaigns  = fundrasing_campaigns.order_by('campaignId')
    items_per_page = 8
    paginator = Paginator(fundrasing_campaigns, items_per_page)
    page = request.GET.get('page')

    try:
        fundrasing_campaigns = paginator.page(page)
    except PageNotAnInteger:
        fundrasing_campaigns = paginator.page(1)
    except EmptyPage:
        fundrasing_campaigns = paginator.page(paginator.num_pages)

    return render(request, 'staff/staff_campaign_dashboard.html', {
        'fundrasing_campaigns':fundrasing_campaigns,
        'total_campaign_count': total_campaign_count})

@staff_required
def staff_pet_dashboard(request):
    query = request.GET.get('q')

    # Retrieve all pets
    pets = Pet.objects.all()

    if query:
        # Filter pets based on the search query
        pets = pets.filter(
            Q(petName__icontains=query) |
            Q(animalType__icontains=query) |
            Q(breed__icontains=query)
        )

    pets = pets.order_by('petId')
    total_pets_count = pets.count()
    items_per_page = 8
    paginator = Paginator(pets, items_per_page)
    page = request.GET.get('page')

    try:
        pets = paginator.page(page)
    except PageNotAnInteger:
        pets = paginator.page(1)
    except EmptyPage:
        pets = paginator.page(paginator.num_pages)

    return render(request, 'staff/staff_pet_dashboard.html', {'pets': pets, 'total_pets_count': total_pets_count})

@staff_required
def add_pet(request):
    if request.method == 'POST':
        pet_form = PetForm(request.POST)
        pet_medical_form = PetMedicalForm(request.POST)
        pet_image_formset = PetImageFormset(request.POST, request.FILES)

        if pet_form.is_valid() and pet_medical_form.is_valid() and pet_image_formset.is_valid():
            pet_instance = pet_form.save()
            
            petmedical = pet_medical_form.save(commit=False)
            petmedical.petId = pet_instance
            petmedical.save()

            for pet_image_form in pet_image_formset:
                pet_image = pet_image_form.save(commit=False)
                pet_image.petId = pet_instance
                pet_image.save()

            return redirect('staff_pet_dashboard')

    else:
        pet_form = PetForm()
        pet_medical_form = PetMedicalForm()
        pet_image_formset = PetImageFormset()
    
    return render(request, 'staff/add_pet.html', 
                  {'pet_form': pet_form, 
                   'pet_medical_form': pet_medical_form,
                   'pet_image_formset': pet_image_formset})

@staff_required
def edit_pet(request, slug):
    pet = get_object_or_404(Pet, slug=slug)
    
    if request.method == 'POST':
        pet_form = PetForm(request.POST, instance=pet)
        medical_form = PetMedicalForm(request.POST, instance=pet.petmedical)
        ImageFormset = PetImageFormset(request.POST, request.FILES, instance=pet)

        if pet_form.is_valid() and medical_form.is_valid() and ImageFormset.is_valid():
            pet_form.save()
            medical_form.save()
            ImageFormset.save()

            # Redirect to the same page or another page as needed
            return redirect('staff_pet_dashboard')
    else:
        pet_form = PetForm(instance=pet)
        medical_form = PetMedicalForm(instance=pet.petmedical)
        ImageFormset = PetImageFormset(instance=pet)

    return render(request, 'staff/edit_pet.html', {
        'pet': pet,
        'pet_form': pet_form,
        'medical_form': medical_form,
        'ImageFormset': ImageFormset,
    })

@staff_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, petId=pet_id)

    if request.method == 'DELETE':
        try:
            pet.delete()
            return JsonResponse({'message': 'Pet deleted successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@staff_required
def add_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES)
        if form.is_valid():
            campaign = form.save()
            # Do any additional processing or redirect as needed
            return redirect('staff_campaign_dashboard')  # Redirect to campaign detail page
    else:
        form = CampaignForm()
    return render(request, 'staff/add_campaign.html', {'form': form})

@staff_required
def edit_campaign(request, campaign_id):
    campaign = get_object_or_404(FundraisingCampaign, campaignId=campaign_id)

    if request.method == 'POST':
        form = CampaignForm(request.POST, request.FILES, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('staff_campaign_dashboard')
    else:
        form = CampaignForm(instance=campaign)

    return render(request, 'staff/edit_campaign.html', {'form': form, 'campaign':campaign})

@staff_required
def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(FundraisingCampaign, campaignId=campaign_id)

    if request.method == 'DELETE':
        try:
            campaign.delete()
            return JsonResponse({'message': 'Campaign deleted successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

# views.py
@staff_required
def review_application(request, application_id):
    application = get_object_or_404(Application, applicationId=application_id)
    
    # Check if an interview already exists for the application
    interview = application.interview_set.first()
    interview_form = InterviewForm(instance=interview) if interview else InterviewForm()

    # Check if a turnover already exists for the application
    turnover = application.turnover_set.first()
    turnover_form = TurnoverForm(instance=turnover) if turnover else TurnoverForm()

    status_form = StatusForm(instance=application)

    if request.method == 'POST':
        interview_form = InterviewForm(request.POST, instance=interview)
        status_form = StatusForm(request.POST, instance=application)
        turnover_form = TurnoverForm(request.POST, instance=turnover)

        if interview_form.is_valid() and status_form.is_valid() and turnover_form.is_valid():
            interview = interview_form.save(commit=False)
            interview.application = application
            interview.interviewedBy = request.user
            interview.save()

            status_instance = status_form.save(commit=False)
            status_instance.save()

            turnover = turnover_form.save(commit=False)
            turnover.application = application
            turnover.save()

            # Check if the application status is set to "Completed"
            if status_instance.status == 'Completed':
                # Create an AdoptedAnimals object
                adopted_animal = AdoptedAnimals(pet=application.pet, user=application.user)
                adopted_animal.save()

            return redirect('staff_application_dashboard')

    context = {
        'application': application,
        'interview_form': interview_form,
        'status_form': status_form,
        'turnover_form': turnover_form,
    }

    return render(request, 'staff/review_application.html', context)