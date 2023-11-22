from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Application, HousePicture, IdPicture, CondoAgreement

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = (
            'adopteeFirstName',
            'adopteeLastName',
            'adopteeHomeAddress',
            'adopteeContactNum',
            'preferredModeOfInterview',
                  )
        
        widgets = {
            'adopteeFirstName' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'adopteeLastName' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'adopteeHomeAddress' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),    
            'adopteeContactNum' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),
            'preferredModeOfInterview' : forms.Select(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}),

        }

        labels = {
            'adopteeFirstName' : 'First Name: ',
            'adopteeLastName' : 'Last Name:',
            'adopteeHomeAddress' : 'Home Address',
            'adopteeContactNum' : 'Contact Number',
            'preferredModeOfInterview' : 'Preferred Mode of Interview:',
        }

class HousePictureForm(forms.ModelForm):
    class Meta:
        model = HousePicture
        fields = ('housePicture',)

        labels = {
            'housePicture' : 'House Picture ',
        }

    def clean_housePicture(self):
        house_picture = self.cleaned_data.get('housePicture')
        if not house_picture:
            raise ValidationError('Please submit at least one house picture.')
        return house_picture

class IdPictureForm(forms.ModelForm):
    class Meta:
        model = IdPicture
        fields = ('validIdPicture',)

        labels = {
            'validIdPicture' : 'Valid ID ',
        }
    
    def clean_validIdPicture(self):
        id_picture = self.cleaned_data.get('validIdPicture')
        if not id_picture:
            raise ValidationError('Please submit at least one valid ID picture.')
        return id_picture

class CondoAgreementForm(forms.ModelForm):
    class Meta:
        model = CondoAgreement
        fields = ('condoAgreement',)

        labels = {
            'condoAgreement' : 'Letter/Contract ',
        }

HousePictureFormSet = inlineformset_factory(Application, HousePicture, form=HousePictureForm, extra=5, can_delete=False)
IdPictureFormSet = inlineformset_factory(Application, IdPicture, form=IdPictureForm, extra=2, can_delete=False)
