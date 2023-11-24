from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TestimonialForm
from .models import Testimonial


# Create your views here.

@login_required
def create_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial_instance = form.save(commit=False)
            testimonial_instance.user = request.user
            testimonial_instance.save()
            return redirect('testimonials')  # Replace with the actual success URL name
    else:
        form = TestimonialForm()

    return render(request, 'testimonials/create_testimonial.html', {'form': form})

def testimonials(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'testimonials/testimonial.html', {'testimonials': testimonials})

def testimonial_detail(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    return render(request, 'testimonials/testimonial_detail.html', {'testimonial': testimonial})