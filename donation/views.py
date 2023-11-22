from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render, get_object_or_404
import random
from django.http import JsonResponse
import requests
from django.contrib.auth.decorators import login_required
from .forms import DonationAmountForm
from django.http import HttpResponse
from django.db.models import Sum

# Create your views here.

def donation_page(request):
    campaigns = list(FundraisingCampaign.objects.all())  # Convert QuerySet to a list

    # Shuffle the campaigns randomly
    random.shuffle(campaigns)

    # Select the first campaign as the featured one
    featured_campaign = campaigns[0]

    context = {'featured_campaign': featured_campaign, 'campaigns': campaigns}
    
    return render(request, 'donation/donation_page.html', context)

def campaign_details(request, campaign_id):
    campaign = get_object_or_404(FundraisingCampaign, campaignId=campaign_id)

    # Get the recent donors for the campaign
    recent_donors = Donation.objects.filter(campaign=campaign).order_by('-donationId')[:5]

    # Calculate the total amount donated
    total_donated = Donation.objects.filter(campaign=campaign).aggregate(Sum('donationAmount'))['donationAmount__sum']

    return render(request, 'donation/donation_profile.html', {
        'campaign': campaign,
        'recent_donors': recent_donors,
        'total_donated': total_donated,
    })

@login_required
def donate(request, campaign_id):
    campaign = get_object_or_404(FundraisingCampaign, campaignId=campaign_id)

    if request.method == 'POST':
        form = DonationAmountForm(request.POST)
        if form.is_valid():
            donation_amount = form.cleaned_data['donationAmount']
            donation = Donation.objects.create(
                campaign=campaign,
                user=request.user,
                donationAmount=donation_amount
            )
            checkout_session_url = create_checkout_session(donation.donationId, donation.donationAmount)
            return redirect(checkout_session_url)
    else:
        form = DonationAmountForm()
    
    return render(request, 'donation/donate.html', {'form': form, 'campaign': campaign})


def create_checkout_session(donationId, donationAmount):
    amount_in_cents = int(donationAmount * 100)
    url = "https://api.paymongo.com/v1/checkout_sessions"

    payload = {
        "data": {
            "attributes": {
                "send_email_receipt": True,
                "show_description": True,
                "show_line_items": True,
                "description": "Donation Fee",
                "line_items": [
                    {
                        "currency": "PHP",
                        "amount": int(amount_in_cents),
                        "description": "Donation Fee",
                        "name": "Donation Fee",
                        "quantity": 1
                    }
                ],
                "payment_method_types": ["gcash", "paymaya", "card"],
                "reference_number": f"{donationId}"
            }
        }
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": "Basic c2tfdGVzdF9NNXJ2ekszdnRZV0Q4cEJmclJIU1VSOVU6"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    checkout_session_url = data['data']['attributes']['checkout_url']
    
    if response.status_code == 200:
        corrected_amount = amount_in_cents/100
        donation = get_object_or_404(Donation, donationId=donationId)
        new_payment = Payment.objects.create(checkout_session_id = data['data']['id'], donation=donation, checkout_url=checkout_session_url, amount=corrected_amount, processed='True')
        new_payment.save()
        
    return checkout_session_url

