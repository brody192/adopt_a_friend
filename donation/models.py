from django.db import models
from users.models import Users

# Create your models here.
def generate_campaign_key():
    last_record = FundraisingCampaign.objects.order_by('-campaignId').first()
    if last_record is not None:
        last_id = int(last_record.campaignId[8:])  # Adjust the index based on your data format
        new_id = last_id + 1
    else:
        new_id = 1
    return f'CAMPAIGN{str(new_id).zfill(4)}'

def generate_donation_key():
    last_record = Donation.objects.order_by('-donationId').first()
    if last_record is not None:
        last_id = int(last_record.donationId[8:])  # Extract the numeric part of the petId
        new_id = last_id + 1
    else:
        new_id = 1
    return f'DONATION{str(new_id).zfill(4)}'

class FundraisingCampaign(models.Model):
    campaignId = models.CharField(max_length=20, default=generate_campaign_key, primary_key=True, unique=True)
    campaignName = models.CharField(max_length=50, null=False, blank=False, unique=True)
    campaignDescription = models.TextField(max_length=800, blank=True, null=True)
    campaignGoal = models.DecimalField(max_digits=8, null=False, decimal_places=2)
    campaignPurpose = models.TextField(max_length=200, null=False, blank=False, default="")
    campaignImage = models.ImageField(upload_to='static/image/campaign_img')

class Message(models.Model):
    from_user = models.ForeignKey(Users, null=False, blank=False, on_delete=models.CASCADE)
    for_campaign = models.ForeignKey(FundraisingCampaign, null=False, blank=False, on_delete=models.CASCADE)
    message = models.TextField(max_length=250, null=False, blank=False)

class Donation(models.Model):
    donationId = models.CharField(max_length=15, default=generate_donation_key, primary_key=True, unique=True)
    campaign = models.ForeignKey(FundraisingCampaign, null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, null=False, blank=False, on_delete=models.CASCADE)
    donationAmount = models.DecimalField(max_digits=8, null=False, decimal_places=2)

    # def save(self, *args, **kwargs):
    #     # Add two zeros to the end of donationAmount for centavos
    #     self.donationAmount *= 100  # Multiply by 100 to add two zeros
    #     self.donationAmount = round(self.donationAmount)  # Round to avoid floating-point precision issues

    #     super(Donation, self).save(*args, **kwargs)
        
class Payment(models.Model):
    checkout_session_id = models.CharField(max_length=150,primary_key=True, unique=True)
    donation = models.ForeignKey(Donation, null=False, blank=False, on_delete=models.CASCADE)
    checkout_url = models.URLField()
    amount = models.DecimalField(max_digits=8, null=False, decimal_places=2)
    processed = models.BooleanField(default=False)