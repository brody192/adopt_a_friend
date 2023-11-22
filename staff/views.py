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
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from PIL import Image
from django.http import FileResponse
import io



# Create your views here.

@staff_required
def staff_dashboard(request):
    # Retrieve completed applications
    completed_applications = Application.objects.filter(status='Completed')

    # Pass the completed applications to the template
    return render(request, 'staff/staff_dashboard.html', {'completed_applications': completed_applications})

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

@staff_required
def review_application(request, application_id):
    # Retrieve the application and related details
    application = get_object_or_404(Application, applicationId=application_id)
    pet_images = PetImage.objects.filter(petId=application.pet)
    house_pictures = HousePicture.objects.filter(applicationId=application)
    id_pictures = IdPicture.objects.filter(applicationId=application)
    condo_agreement = CondoAgreement.objects.filter(applicationId=application).first()

    # Handle form submission
    if request.method == 'POST':
        form = ReviewApplicationForm(request.POST)
        if form.is_valid():
            # Update application details based on the form data
            application.status = form.cleaned_data['status']
            application.staffComment = form.cleaned_data['staffComment']
            application.interviewDate = form.cleaned_data['interviewDate']
            application.interviewTime = form.cleaned_data['interviewTime']
            application.inPersonVisitDate = form.cleaned_data['inPersonVisitDate']
            application.inPersonVisitTime = form.cleaned_data['inPersonVisitTime']
            application.save()

            # Redirect to a success page or the same page
            return redirect('staff_application_dashboard')

    else:
        # Display the form for staff to fill in
        form = ReviewApplicationForm(initial={
            'status': application.status,
            'staff_comment': application.staffComment,
            'interview_date': application.interviewDate,
            'interview_time': application.interviewTime,
            'in_person_visit_date': application.inPersonVisitDate,
            'in_person_visit_time': application.inPersonVisitTime,
        })

    context = {
        'application': application,
        'form': form,
    }

    return render(request, 'staff/review_application.html', context)



def generate_pet_data_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pet_data_report.pdf"'
    buffer = BytesIO()
    pdf_doc = SimpleDocTemplate(buffer, pagesize=landscape(legal))

    title_for_pets = "Pet Information"
    title_for_medical = "Pet Medical Information"
    report_title = "Pet Report"
    report_description = "This file contains a comprehensive report about the information of pets along with their medical information. The information listed below are from the adoptable pets in Quezon City Animal Care and Adoption Center's animal shelter."
    system_generated_report = "This is a system generated report."

    #PET
    pet_data = []
    pet_data.append([
        'Pet ID',
        'Pet Name',
        'Animal Type',
        'Breed',
        'Pet Age',
        'Pet Gender',
        'Pet Size',
        'Pet Color',
        'Pet Personality',
        'Date Acquired',
        'Is the Pet Trained?'
    ])

    for pet in Pet.objects.all():
        pet_data.append([
            pet.petId,
            pet.petName,
            pet.animalType,
            pet.breed,
            pet.petAge,
            pet.petGender,
            pet.petSize,
            pet.petColor,
            pet.petPersonality,
            pet.dateAcquired,
            pet.isTrained,
        ])

    
    #PET MEDICAL
    pet_medical_data = []

    pet_medical_data.append([
        'Pet Name',
        'Weight',
        'Is the Pet Vaccinated?',
        'Is the Pet Neutured/Spayed?',
        'Health Condition',
        'Disease'
    ])

    for pet_medical in PetMedical.objects.all():
        pet_medical_data.append([
            pet_medical.petId.petName,
            pet_medical.petWeight,
            pet_medical.isVaccinated,
            pet_medical.isNeutered_or_Spayed,
            pet_medical.healthCondition,
            pet_medical.disease,
        ])
    
    pet_table = create_table(pet_data, Pet._meta.fields, "Pet Data")
    pet_medical_table = create_table(pet_medical_data, PetMedical._meta.fields, "Pet Medical Data")

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    
    # Create a style with center alignment
    center_style = ParagraphStyle(
        'Centered',
        parent=normal_style,
        alignment=TA_CENTER,
        fontSize = 14,
        spaceBefore=50,  # Adjust the top padding
        spaceAfter=30    # Adjust the bottom padding
    )

    style_for_report_title = ParagraphStyle(
        'Centered',
        fontSize = 30,
        parent=normal_style,
        spaceBefore=0,  # Adjust the top padding
        spaceAfter=30    # Adjust the bottom padding
    )

    style_for_report_description = ParagraphStyle(
        'Centered',
        fontSize = 12,
        parent=normal_style,
        spaceBefore=0,  # Adjust the top padding
        spaceAfter=30,    # Adjust the bottom padding
    )

    style_for_system_generated_message = ParagraphStyle(
        'Centered',
        fontSize = 12,
        parent=normal_style,
        spaceBefore=50,  # Adjust the top padding
        spaceAfter=30,    # Adjust the bottom padding
        alignment = TA_CENTER
    )

    centered_title_for_pets = Paragraph(title_for_pets, center_style)
    centered_title_for_medical = Paragraph(title_for_medical, center_style)
    report_title_title = Paragraph(report_title, style_for_report_title)
    description = Paragraph(report_description, style_for_report_description)
    system_generated_message = Paragraph(system_generated_report, style_for_system_generated_message)

    pdf_elements = [report_title_title, description ,centered_title_for_pets, pet_table, centered_title_for_medical, pet_medical_table, system_generated_message]
    pdf_doc.build(pdf_elements)

    pdf_value = buffer.getvalue()
    buffer.close()
    response.write(pdf_value)

    return response

def create_table(data, fields ,title):
    # headers = [field.name for field in fields]
    table_data = data
    table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 14),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    table.setStyle(style)
    return table

def generate_application_report(request, application_id):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)

    # Load the models
    application = get_object_or_404(Application, applicationId=application_id)

    # Draw the application details
    p.drawString(270, 750, f'{application.adopteeFirstName} {application.adopteeLastName}')
    p.drawString(270, 735, f'{application.applicationId}')
    # ... add more details as needed

    # Draw the application picture
    image_path = application.picture.path
    application_image = Image.open(image_path)
    application_image = application_image.resize((150, 150))  # Force resize the image
    p.drawInlineImage(application_image, 70, 610)

    # Move to the next page
    p.showPage()

    # Close the PDF object cleanly, and we're done.
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'application_{application_id}.pdf')

