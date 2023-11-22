from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login as auth_login, logout
from .forms import UsersForm, LoginForm, ProfilePictureUpdateForm, UserUpdateForm, PreferenceForm
from verify_email.email_handler import send_verification_email
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib import messages
from django.urls import reverse
import os
from pets.models import Application
from django.conf import settings

# Create your views here.

@unauthenticated_user
def create_user(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        preference_form = PreferenceForm(request.POST)

        if form.is_valid() and preference_form.is_valid():
            inactive_user = send_verification_email(request, form)
            user = form.save()
            
            preference = preference_form.save(commit=False)
            preference.adopter = user
            preference.save()

            return redirect('/sent_email/')
    else:
        form = UsersForm()
        preference_form = PreferenceForm()

    return render(request, 'users/signup.html', {
        'form': form, 
        'preference_form': preference_form, 
        })

@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if request.user.is_staff:
                return redirect('staff_dashboard')
            else:
                return redirect('index')
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

def sent_email(request):
    return render(request, 'users/sent_email.html')

@login_required
def profile(request, slug, id):
    user = get_object_or_404(Users, slug=slug)

    try:
        adopter = Users.objects.get(pk=id)
        preference = Preference.objects.get(adopter=adopter)
        applications = Application.objects.filter(user=adopter)
    except Users.DoesNotExist:
        adopter = None
        preference = None
        applications = None
    except Preference.DoesNotExist:
        preference = None
        applications = None

    context = {
        'user': user,
        'adopter': adopter,
        'preference': preference,
        'applications': applications,
    }

    return render(request, 'users/profile.html', context)

@login_required
def update_profile(request, slug, id):
    user = get_object_or_404(Users, slug=slug, id=id)
    
    if request.method == 'POST':
        update_user_form = UserUpdateForm(request.POST, instance=request.user)
        update_profile_form = ProfilePictureUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if update_user_form.is_valid() and update_profile_form.is_valid():
            # Get the previous profile picture
            previous_picture = user.profile.image
            # Check if the previous picture is the default one
            is_default_picture = str(previous_picture) == 'default.png'

            # Check if a new image has been provided
            new_profile_picture = update_profile_form.cleaned_data.get('image')

            # If a new picture is provided and the previous one is not the default
            if new_profile_picture and not is_default_picture:
                # Delete the previous profile picture if it is not the default one
                full_path = os.path.join(settings.MEDIA_ROOT, str(previous_picture))
                if os.path.exists(full_path):
                    os.remove(full_path)

            # Save the updated user form
            update_user_form.save()
            # Save the updated profile form
            profile_instance = update_profile_form.save(commit=False)
            profile_instance.user = request.user
            profile_instance.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect(user.get_absolute_url())
        
    else:
        update_user_form = UserUpdateForm(instance=request.user)
        update_profile_form = ProfilePictureUpdateForm(instance=request.user.profile)
    
    context = {
        'update_user_form': update_user_form,
        'update_profile_form': update_profile_form,
        'user': user,
    }

    return render(request, 'users/update_profile.html', context)

