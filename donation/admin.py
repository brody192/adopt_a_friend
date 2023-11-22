from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(FundraisingCampaign)
admin.site.register(Message)
admin.site.register(Donation)
admin.site.register(Payment)
