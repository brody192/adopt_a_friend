from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = (
            'caption',
            'testimonial',
            'image',
                  )
        
        widgets = {
            'caption' : forms.TextInput(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
            'testimonial' : forms.Textarea(attrs={'class': 'mt-2 border-2 border-black w-full px-6 py-3 mb-2 rounded-lg font-medium'}), 
        }

        labels = {
            'testimonial' : 'Write your success story here ',
            'image' : 'Photo with your pet',
        }