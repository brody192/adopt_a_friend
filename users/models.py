from django.db import models
from django.utils import timezone
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image
from datetime import date


COLOR_CHOICES = (
    ('Black', 'Black'),
    ('White', 'White'),
    ('Gray', 'Gray'),
    ('Brown', 'Brown'),
    ('Orange', 'Orange'),
    ('Cream', 'Cream'),
    ('Bi-color', 'Bi-color'),
    ('Tricolor', 'Tricolor'),
    ('Any', 'Any'),
)

BREED = (
    ('Puspin', 'Puspin'),
    ('Aspin', 'Aspin'),
    ('Any', 'Any'),
)

PERSONALITY_CHOICES = (
    ('Playful', 'Playful'),
    ('Cuddly', 'Cuddly'),
    ('Energetic', 'Energetic'),
    ('Laid_back', 'Laid-back'),
    ('Curious', 'Curious'),
    ('Social', 'Social'),
    ('Independent', 'Independent'),
    ('Shy/Timid', 'Shy/Timid'),
    ('Bold/Confident', 'Bold/Confident'),
    ('Intelligent', 'Intelligent'),
    ('Mischievous', 'Mischievous'),
    ('Reserved', 'Reserved'),
    ('Protective', 'Protective'),
    ('Adventurous', 'Adventurous'),
    ('Affectionate', 'Affectionate'),
    ('Patient', 'Patient'),
    ('Stubborn', 'Stubborn'),
    ('Gentle', 'Gentle'),
    ('Sociable', 'Sociable'),
    ('Talkative', 'Talkative'),
)

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others')
)

PET_GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Any', 'Any'),
)

ANIMAL_TYPES_CHOICES = (
    ('Dog', 'Dog'),
    ('Cat', 'Cat'),
    ('Any', 'Any'),
)

PET_AGE_CHOICES = (
    ('Puppy/Kitten', 'Puppy/Kitten'),
    ('Young', 'Young'),
    ('Adult', 'Adult'),
    ('Senior', 'Senior'),
    ('Any', 'Any'),
)

PET_SIZE_CHOICES = (
    ('Extra Small', 'Extra Small'),
    ('Small', 'Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large'),
    ('Any', 'Any'),
)

HEALTH_CONDITIONS = (
    ('Healthy', 'Healthy'),
    ('With Disease/Illness', 'With Disease/Illness'),
    ('Chronic Condition', 'Chronic Condition'),
    ('Under Treatment', 'Under Treatment'),
    ('Recovering', 'Recovering'),
    ('Injured', 'Injured'),
    ('Behavioral Issues', 'Behavioral Issues'),
    ('Senior Care', 'Senior Care'),
    ("I don't mind", "I don't mind"),
)

GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
)

def generate_preference_key():
    last_record = Preference.objects.order_by('-preferenceId').first()
    if last_record is not None:
        last_id = int(last_record.preferenceId[3:])  # Extract the numeric part of the petId
        new_id = last_id + 1
    else:
        new_id = 1
    return f'PRF{str(new_id).zfill(4)}'

class CustomAccountManager(BaseUserManager):
    # ------ FOR CREATING USER ACCOUNTS ------ #
    def create_user(self, email, password, first_name, last_name, gender, age, date_of_birth, home_address, contact_num, **other_fields):
        email = self.normalize_email(email)

        if not email:
            raise ValueError("Email address is required")

        user = self.model(email=email, first_name=first_name, last_name=last_name, gender=gender, age=age, date_of_birth=date_of_birth, home_address=home_address, contact_num=contact_num, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    # ------ FOR CREATING SUPERUSER/ADMIN ACCOUNTS ------ #

    def create_superuser(self, email=None, password=None, first_name=None, last_name=None, gender=None, age=None, date_of_birth=None, home_address=None, contact_num=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Staff must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        return self.create_user(email, password, first_name, last_name, gender, age, date_of_birth, home_address, contact_num, **other_fields)

class Users(AbstractBaseUser, PermissionsMixin):
     
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    gender = models.CharField(max_length=20, blank=False, null=False, choices=GENDER_CHOICES, default="")
    date_of_birth = models.DateField(blank=False, null=False)
    home_address = models.CharField(max_length=200, blank=False, null=False)
    contact_num = models.CharField(max_length=15, blank=False, null=False)
    user_bio = models.TextField(max_length=500, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender' ,'date_of_birth', 'home_address', 'contact_num']

    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"slug": self.slug, "id": self.id})
    
    def get_absolute_url_for_update(self):
        return reverse("update_profile", kwargs={"slug": self.slug, "id": self.id})

    def save(self, *args, **kwargs):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        self.age = age

        self.slug = slugify(f"{self.first_name} {self.last_name}")
        super(Users, self).save(*args, **kwargs)

        # CURRENT/GOAL 1000/10000

class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    image = models.ImageField(default='static/default.png', upload_to='static/profile_pics')

    def __str__(self):
        return f'{self.user.first_name} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 224 or img.width > 224:
            output_size = (224,224)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Preference(models.Model):
    
    preferenceId = models.CharField(max_length=10, default=generate_preference_key, primary_key=True, unique=True)
    adopter = models.ForeignKey(Users, null=False, blank=False, on_delete=models.CASCADE)
    preferredAnimalType = models.CharField(max_length=20, choices=ANIMAL_TYPES_CHOICES, null=False, blank=False, default="")
    preferredBreed = models.CharField(max_length=20, choices=BREED, null=False, blank=False, default="Any")
    preferredAge = models.CharField(max_length=20, choices=PET_AGE_CHOICES, null=False, blank=False, default="")
    preferredGender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=False, blank=False, default="")
    preferredSize = models.CharField(max_length=20, choices=PET_SIZE_CHOICES, null=False, blank=False, default="")
    preferredColor = models.CharField(max_length=20, choices=COLOR_CHOICES, null=False, blank=False, default="")
    preferredSpayedorNeutered = models.BooleanField()
    preferredHealthCondition = models.CharField(max_length=30, null=False, choices=HEALTH_CONDITIONS, default="")
    preferredPersonality = models.CharField(max_length=50, choices=PERSONALITY_CHOICES, blank=False, null=False, default="")
    