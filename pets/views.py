from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .recommendation import recommend_pets
from users.models import Preference
from django.utils import timezone


# Create your views here.

def pet_profile(request, petId, slug):
    pet = get_object_or_404(Pet, petId=petId, slug=slug)
    medical = get_object_or_404(PetMedical, petId=pet)
    images = PetImage.objects.filter(petId=pet)

    context = {
            'pet': pet,
            'medical': medical,
            'images': images,
        }

    return render(request, 'pets/pet_profile.html', context)

from .recommendation import recommend_pets

def pet_page(request):
    query = request.GET.get('q')
    pets = Pet.objects.all().order_by('petId')
    recommended_pets = []

    if request.user.is_authenticated:
        try:
            # Try to get the user's preferences
            user_pref = Preference.objects.get(adopter=request.user)
            # Get recommended pets for the authenticated user
            recommended_pets = recommend_pets(request.user)
        except Preference.DoesNotExist:
            # Handle the case where the user has no preferences
            pass

    if query:
        # Filter pets based on the search query
        pets = pets.filter(
            Q(petName__icontains=query) |
            Q(animalType__icontains=query) |
            Q(breed__icontains=query) |
            Q(petAge__icontains=query) |
            Q(petGender__icontains=query) 
        )

    return render(request, 'pets/adoptme.html', {'pets': pets, 'recommended_pets': recommended_pets})

@login_required
def application(request, slug):
    pet = get_object_or_404(Pet, slug=slug)
    user = request.user

    existing_application = Application.objects.filter(pet=pet, user=user).first()
    if existing_application:
        # You can redirect to a page indicating that the user has already applied for this pet
        return redirect('application_duplication')
    
    week_ago = timezone.now() - timezone.timedelta(weeks=1)
    user_applications_last_week = Application.objects.filter(user=user, created_at__gte=week_ago).count()

    if user_applications_last_week >= 2:
        # You can redirect to a page indicating that the user has reached the limit for the week
        return redirect('submission_exceeded')

    if request.method == 'POST':
        application_form = ApplicationForm(request.POST)
        house_picture_formset = HousePictureFormSet(request.POST, request.FILES, prefix='house_picture')
        id_picture_formset = IdPictureFormSet(request.POST, request.FILES, prefix='id_picture')
        condo_agreement_form = CondoAgreementForm(request.POST, request.FILES)

        if (
            application_form.is_valid()
            and house_picture_formset.is_valid()
            and id_picture_formset.is_valid()
            and condo_agreement_form.is_valid()
        ):
            # Save the main application form
            application_instance = application_form.save(commit=False)
            application_instance.pet = pet
            application_instance.user = user
            application_instance.save()

            # Save the related forms in the formsets
            house_picture_formset.instance = application_instance
            house_picture_formset.save()

            id_picture_formset.instance = application_instance
            id_picture_formset.save()

            # Save the condo agreement form if provided
            if request.FILES.get('condoAgreement'):
                condo_agreement_instance = condo_agreement_form.save(commit=False)
                condo_agreement_instance.applicationId = application_instance
                condo_agreement_instance.save()

            # Redirect to a success page or any other desired page
            return redirect('submitted')  # Replace 'success_page' with the actual URL or name of the success page

    else:
        # Pass the logged-in user to the form
        application_form = ApplicationForm(initial={'adopteeFirstName': user.first_name,
                                                    'adopteeLastName': user.last_name,
                                                    'adopteeHomeAddress': user.home_address,
                                                    'adopteeContactNum': user.contact_num})
        house_picture_formset = HousePictureFormSet(prefix='house_picture')
        id_picture_formset = IdPictureFormSet(prefix='id_picture')
        condo_agreement_form = CondoAgreementForm()

    context = {
        'pet': pet,
        'user': user,
        'application_form': application_form,
        'house_picture_formset': house_picture_formset,
        'id_picture_formset': id_picture_formset,
        'condo_agreement_form': condo_agreement_form,
    }

    return render(request, 'pets/application.html', context)

@login_required
def submitted(request):
    return render(request, 'pets/application_submitted_successfuly.html')

@login_required
def submission_exceeded(request):
    return render(request, 'pets/application_limit_exceeded.html')

@login_required
def application_duplication(request):
    return render(request, 'pets/application_already_submitted.html')
