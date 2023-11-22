from django import forms
from .models import Donation

class DonationAmountForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donationAmount']

        widgets = {
            'donationAmount': forms.NumberInput(
                attrs={
                    'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium',
                    'placeholder': 'Enter donation amount...',
                }
            ),
        }

        labels = {
            'donationAmount': 'Enter donation amount:',
        }


    