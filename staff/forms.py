from django import forms
from pets.models import *
from donation.models import *
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = (
            'petName',
            'animalType',
            'breed',
            'petAge',
            'petGender',
            'petSize',
            'petPersonality',
            'petColor',
            'petDescription',
            'isTrained',
        )

        widgets = {
            'petName' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'animalType' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'breed' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'petAge' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'petGender' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'petSize' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'petPersonality': forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'petColor': forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'petDescription' : forms.Textarea(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'isTrained' : forms.CheckboxInput(attrs={'class' : 'ml-4'})
        }

        labels = {
            'petName' : 'Pet Name:',
            'animalType' : 'Animal Type:',
            'breed' : 'Breed:',
            'petAge' : 'Pet Age:',
            'petGender' : 'Pet Gender:',
            'petSize' : 'Pet Size:',
            'petPersonality': 'Pet Personality:',
            'petColor': 'Pet Color:',
            'petDescription' : 'Pet Description:',
            'isTrained' : 'Is the pet trained? (check the box if yes):'
        }
    
    # PUT VALIDATIONS HERE

class PetMedicalForm(forms.ModelForm):
    class Meta:
        model = PetMedical
        fields = (
            'petWeight',
            'isVaccinated',
            'isNeutered_or_Spayed',
            'comment',
        )
    
        widgets = {
            'petWeight' : forms.NumberInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'isVaccinated' : forms.CheckboxInput(attrs={'class' : 'ml-4'}),
            'isNeutered_or_Spayed' : forms.CheckboxInput(attrs={'class' : 'ml-4'}),
            'comment' : forms.Textarea(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
        }

        labels = {
            'petWeight' : 'Weight (in KG):',
            'isVaccinated' : 'Is the pet vaccinated? (check the box if yes):',
            'isNeutered_or_Spayed' :  'Is the pet spayed/neutered? (check the box if yes):',
            'comment' : 'Vet Comment:'
        }
    
     # PUT VALIDATIONS HERE

class PetImageForm(forms.ModelForm):
    class Meta:
        model = PetImage
        fields = (
            'petImage',
        )

        labels = {
            'petImage' : 'Pet Image'
        }
    
     # PUT VALIDATIONS HERE

PetImageFormset = inlineformset_factory(Pet, PetImage, form=PetImageForm, extra=3, can_delete=False, max_num=3)

# ------------------------------ CAMPAIGN FORMS ----------------------------- #

class CampaignForm(forms.ModelForm):
    class Meta:
        model = FundraisingCampaign
        exclude = ['campaignId']

        widgets = {
            'campaignName' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'campaignDescription' : forms.Textarea(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'campaignGoal' : forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'campaignPurpose' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
        }

        labels = {
            'campaignName' : 'Campaign Name:', 
            'campaignDescription' : 'Campaign Description:',
            'campaignGoal' : 'Campaign Goal:',
            'campaignImage': 'Campaign Image:',
            'campaignPurpose' : 'Purpose of the Campaign', 
        }

     # PUT VALIDATIONS HERE

# ------------------------------ REVIEW APPLICATION FORMS ----------------------------- #

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            'interviewDate',
            'interviewTime',
        ]

        widgets = {
            'interviewDate': forms.DateInput(attrs={'type': 'date', 'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'interviewTime' : forms.TimeInput(attrs={'type': 'time', 'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 

        }

        labels = {
            'interviewDate': 'Date of Online Interview',
            'interviewTime' : 'Time of Online Interview',
        }

class TurnoverForm(forms.ModelForm):
    class Meta:
        model = Turnover
        fields = [
            'turnoverDate',
            'turnoverTime',
        ]

        widgets = {
            'turnoverDate': forms.DateInput(attrs={'type': 'date', 'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'turnoverTime' : forms.TimeInput(attrs={'type': 'time', 'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 

        }

        labels = {
            'turnoverDate': 'Date of Pet Turnover',
            'turnoverTime' : 'Time of Pet Turnover',
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'status',
        ]

        widgets = {
            'status': forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
        }


