from django.db import models
from users.models import Users
from django.db.models import F
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from PIL import Image

COLOR_CHOICES = (
    ('Black', 'Black'),
    ('White', 'White'),
    ('Gray', 'Gray'),
    ('Brown', 'Brown'),
    ('Orange', 'Orange'),
    ('Cream', 'Cream'),
    ('Bi-color', 'Bi-color'),
    ('Tricolor', 'Tricolor')
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
    ('Other', 'Other')
)

PET_AGE_CHOICES = (
    ('Puppy/Kitten', 'Puppy/Kitten'),
    ('Young', 'Young'),
    ('Adult', 'Adult'),
    ('Senior', 'Senior')
)

ANIMAL_TYPES_CHOICES = (
    ('Dog', 'Dog'),
    ('Cat', 'Cat'),
    ('Others', 'Others')
)

PET_SIZE_CHOICES = (
    ('Extra Small', 'Extra Small'),
    ('Small', 'Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large')
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
)

APPLICATION_STATUS = (
    ('Pending', 'Pending'),
    ('Interviewing', 'Interviewing'),
    ('Accepted', 'Accepted'),
    ('On Hold', 'On Hold'),
    ('Rejected', 'Rejected'),
    ('Evaluating', 'Evaluating'),
    ('Completed', 'Completed'),
)

INTERVIEW_MODE = (
    ('Online', 'Online'),
    ('On-site', 'On-site'),
)
def generate_pet_key():
    last_record = Pet.objects.order_by('-petId').first()
    if last_record is not None:
        last_id = int(last_record.petId[3:])  # Extract the numeric part of the petId
        new_id = last_id + 1
    else:
        new_id = 1
    return f'PET{str(new_id).zfill(4)}'

def generate_med_key():
    last_record = Pet.objects.order_by('-medId').first()
    if last_record is not None:
        new_id = F('medId') + 1
    else:
        new_id = 1
    return f'MED{str(new_id).zfill(4)}'

def generate_application_key():
    last_record = Application.objects.order_by('-applicationId').first()
    if last_record is not None:
        last_id = int(last_record.applicationId[3:])  # Extract the numeric part of the petId
        new_id = last_id + 1
    else:
        new_id = 1
    return f'APP{str(new_id).zfill(4)}'

class Pet(models.Model):
    petId = models.CharField(max_length=10, default=generate_pet_key, primary_key=True, unique=True)
    petName = models.CharField(max_length=50, null=False, blank=False, unique=True)
    animalType = models.CharField(max_length=20, choices=ANIMAL_TYPES_CHOICES, null=False, blank=False)
    breed = models.CharField(max_length=50, null=False, blank=False)
    petAge = models.CharField(max_length=50, null=False, blank=False, choices=PET_AGE_CHOICES)
    petGender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=False, blank=False, default="")
    petSize = models.CharField(max_length=20, choices=PET_SIZE_CHOICES, null=False, blank=False)
    petColor = models.CharField(max_length=20, choices=COLOR_CHOICES, null=False, blank=False, default="")
    petDescription = models.TextField(max_length=500, blank=True, null=True)
    petPersonality = models.CharField(max_length=50, choices=PERSONALITY_CHOICES, blank=False, null=False, default="")
    dateAcquired = models.DateField(blank=False, null=False, default=timezone.now)
    isTrained = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    
    def get_absolute_pet_url(self):
        return reverse("pet_profile", kwargs={"slug": self.slug, "petId": str(self.petId)})
    
    def get_absolute_pet_url_for_update(self):
        return reverse("edit_pet", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.petName}")
        super(Pet, self).save(*args, **kwargs)

class PetImage(models.Model):
    petId = models.ForeignKey('Pet', null=False, blank=False, on_delete=models.CASCADE)
    petImage = models.ImageField(upload_to='static/pet_pics')

    def save(self, *args, **kwargs):
        try:
            this = PetImage.objects.get(id=self.id)
            if this.petImage != self.petImage:
                this.petImage.delete(save=False)
        except PetImage.DoesNotExist:
            pass

        super(PetImage, self).save(*args, **kwargs)

class PetMedical(models.Model):
    petId = models.OneToOneField(Pet, null=False, blank=False, on_delete=models.CASCADE)
    petWeight = models.IntegerField(blank=False, null=False)
    isVaccinated = models.BooleanField()
    isNeutered_or_Spayed = models.BooleanField()
    healthCondition = models.CharField(max_length=30, null=False, choices=HEALTH_CONDITIONS)
    disease = models.CharField(max_length=100, null=False)
    comment = models.TextField(max_length=500, blank=True, null=True)

class Application(models.Model):
    applicationId = models.CharField(max_length=10, default=generate_application_key, primary_key=True, unique=True)
    pet = models.ForeignKey(Pet, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, null=False, on_delete=models.CASCADE)
    adopteeFirstName = models.CharField(max_length=50, null=False, blank=False)
    adopteeLastName = models.CharField(max_length=50, null=False, blank=False)
    adopteeHomeAddress = models.CharField(max_length=300, null=False, blank=False)
    adopteeContactNum = models.CharField(max_length=15, null=False, blank=False)
    picture = models.ImageField(blank=False, null=False, upload_to='static/application_pics', default="static/default.png")
    status = models.CharField(max_length=50, choices=APPLICATION_STATUS ,null=False, blank=False, default="Pending")
    preferredModeOfInterview =  models.CharField(max_length=50, choices=INTERVIEW_MODE ,null=False, blank=False, default="")
    modeOfInterview =  models.CharField(max_length=50, choices=INTERVIEW_MODE ,null=False, blank=False, default="")
    staffComment = models.TextField(max_length=300, null=False, blank=True, default='')
    interviewDate = models.DateField(null=True, blank=True)
    interviewTime = models.TimeField(null=True, default=None, blank=True)
    inPersonVisitDate = models.DateField(null=True, blank=True)
    inPersonVisitTime = models.TimeField(null=True, default=None, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

class HousePicture(models.Model):
    applicationId = models.ForeignKey(Application, null=False, on_delete=models.CASCADE)
    housePicture = models.ImageField(blank=False, null=False, upload_to='static/application_pics')

class IdPicture(models.Model):
    applicationId = models.ForeignKey(Application, null=False, on_delete=models.CASCADE)
    validIdPicture = models.ImageField(blank=False, null=False, upload_to='static/application_pics')

class CondoAgreement(models.Model):
    applicationId = models.ForeignKey(Application, null=False, on_delete=models.CASCADE)
    condoAgreement = models.FileField(upload_to='static/application_files', null=True, blank=True)