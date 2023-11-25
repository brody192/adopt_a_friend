from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Application, HousePicture, IdPicture, CondoAgreement, CompletionForm


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = (
            'adopterFirstName',
            'adopterLastName',
            'adopterHomeAddress',
            'adopterContactNum',
                  )
        
        widgets = {
        'adopterFirstName': forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium', 'required': 'required'}),
        'adopterLastName': forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium', 'required': 'required'}),
        'adopterHomeAddress': forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium', 'required': 'required'}),
        'adopterContactNum': forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium', 'required': 'required'}),
        }

        labels = {
            'adopterFirstName' : 'First Name: ',
            'adopterLastName' : 'Last Name:',
            'adopterHomeAddress' : 'Home Address',
            'adopterContactNum' : 'Contact Number',
        }

class HousePictureForm(forms.ModelForm):
    class Meta:
        model = HousePicture
        fields = ('housePicture',)

    def __init__(self, *args, **kwargs):
        super(HousePictureForm, self).__init__(*args, **kwargs)
        self.fields['housePicture'].required = True

class IdPictureForm(forms.ModelForm):
    class Meta:
        model = IdPicture
        fields = ('validIdPicture',)

    def __init__(self, *args, **kwargs):
        super(IdPictureForm, self).__init__(*args, **kwargs)
        self.fields['validIdPicture'].required = True

class CondoAgreementForm(forms.ModelForm):
    class Meta:
        model = CondoAgreement
        fields = ('condoAgreement',)

        labels = {
            'condoAgreement' : 'Letter/Contract ',
        }

class CompletionForm(forms.ModelForm):
    class Meta:
        model = CompletionForm
        fields = ('agree',)

        labels = {
            'agree' : 'I agree to terms and conditions.',
        }

