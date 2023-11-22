from django import forms
from django.forms import inlineformset_factory
from .models import Users, Profile, Preference
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError


class UsersForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
        help_text="Your password should contain at least 8 characters."
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
        help_text="Please enter the same password as above, for verification."
    )
    
    #VALIDATION FOR CONTACT NUM
    def clean_contact_num(self):
        value = self.cleaned_data['contact_num']

        if len(value) != 11 or not value.isdigit():
            raise ValidationError(
                "Contact number must be 11 digits long and contain only digits."
            )

        return value

    #VALIDATION FOR FIRST NAME
    def clean_first_name(self):
        value = self.cleaned_data['first_name']

        if not value.isalpha() and not value.isspace():
            raise ValidationError("First name must contain only letters.")

        return value

    #VALIDATION FOR LAST NAME
    def clean_last_name(self):
        value = self.cleaned_data['last_name']

        if not value.isalpha() and not value.isspace():
            raise ValidationError("Last name must contain only letters.")

        return value
    
     #PUT VALIDATIONS HERE

    class Meta:
        model = Users
        fields = (
            'email', 
            'first_name', 
            'last_name', 
            'gender', 
            'date_of_birth', 
            'home_address', 
            'contact_num',
        )

        widgets = {
            'email' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'first_name' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'last_name' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),   
            'gender' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'home_address' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'date_of_birth' : forms.DateInput(attrs={'type': 'date', 'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'contact_num' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
        }

        labels = {
            'email' : 'Email: ',
            'first_name' : 'First Name:',
            'last_name' : 'Last Name',
            'gender' : 'Gender',
            'home_address' : 'Home Address',
            'date_of_birth' : 'Birth Date:',
            'contact_num' : 'Contact Number:',
        }



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your email',
        'class': 'w-full px-6 py-3 mb-2 border border-slate-600 rounded-lg font-medium'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full px-6 py-3 mb-2 border border-slate-600 rounded-lg font-medium'
    }))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = (
            'home_address', 
            'contact_num',
            'user_bio',
        )

        widgets = {
            'home_address' : forms.TextInput(attrs={'class': 'w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'contact_num' : forms.TextInput(attrs={'class': 'w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'user_bio' : forms.Textarea(attrs={'class': 'w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
        }

        labels = {
            'home_address': 'Home Address:',  
            'contact_num': 'Contact Number:',
            'user_bio': 'User Bio:',
        }
    
class ProfilePictureUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'image',
        )

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        exclude = ['preferenceId', 'adopter']

        widgets = {
            'preferredAnimalType' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'preferredBreed' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'preferredAge' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'preferredGender' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'preferredSize' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),             
            'preferredColor': forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'preferredHealthCondition' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'preferredPersonality': forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'preferredSpayedorNeutered' : forms.CheckboxInput(attrs={'class' : 'ml-4'}),
        }

        labels = {
            'preferredAnimalType': 'Preferred Animal Type:',
            'preferredBreed': 'Preferred Breed:',
            'preferredAge': 'Preferred Age of the Pet:',
            'preferredGender': 'Preferred Gender of the Pet:',
            'preferredSize': 'Preferred Size of the Pet:',
            'preferredColor': 'Preferred Color of the Pet:',
            'preferredSpayedorNeutered': 'Preference for a Spayed or Neutered Pet (check if yes):',
            'preferredHealthCondition': 'Preferred Health Condition of the Pet:',
            'preferredPersonality': 'Preferred Pet Personality:'
        }