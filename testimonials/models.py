from django.db import models
from users.models import Users
from django.utils import timezone

# Create your models here.

class Testimonial(models.Model):
    user = models.ForeignKey(Users, null=False, blank=False, on_delete=models.CASCADE)
    caption =  models.CharField(max_length=100 ,null=False, blank=False, default='')
    testimonial = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='static/testimonial_pics')

