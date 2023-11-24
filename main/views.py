from django.shortcuts import render
from pets.models import Pet
from donation.models import FundraisingCampaign

# Create your views here.

def index(request):
    pets = Pet.objects.order_by('?')[:5]
    campaign = FundraisingCampaign.objects.order_by('?').first()
    context = {'pets': pets, 'campaign': campaign}
    return render(request, "main/index.html", context)

def login(response):
    return render(response, "main/login.html")

def about(response):
    return render(response, "main/about.html")

def error_404(request, exception):
    return render(request, 'main/404.html', status=404)
