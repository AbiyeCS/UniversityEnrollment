from django.db import models
from authentication.models import *

# Create your models here.


class UniversityProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    display_image = models.CharField(max_length=255, null=True, blank=True)
    display_image_file = models.ImageField(upload_to='university_images/', null=True, blank=True)
    site_url = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.name

    def get_weights_str(self):
        weight_object = UniversityAIWeight.objects.filter(university_profile=self).first()
        return f"Grade:{weight_object.gpa_weight}|Sports:{weight_object.sports_interest_weight}|ExtraCircular:{weight_object.extracurricular_interest_weight}"

    def get_last_app_date(self):
        try:
            value = UniversitySession.objects.filter(university=self).first().application_deadline
        except:
            value = "Not decided yet"

        return value

    def get_session_start_date(self):
        try:
            value = UniversitySession.objects.filter(university=self).first().start_date
        except:
            value = "Not decided yet"
        return  value

    def get_display_image(self):
        try:
            if self.display_image:
                value = self.display_image
            elif self.display_image_file.url:
                value = self.display_image_file.url
            else:
                value = '/static/assets/images/1.jpg'
        except Exception as e:
            value = '/static/assets/images/1.jpg'
        return value


class UniversitySession(models.Model):
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    start_date = models.DateField()
    application_deadline = models.DateField()


class Discipline(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(models.Model):
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    short_description = models.TextField()
    discipline = models.ManyToManyField(Discipline)
    fee = models.ManyToManyField('Fee', blank=True)
    requirements = models.TextField(null=True, blank=True)
    university_course_url = models.CharField(max_length=255, null=True, blank=True)
    taught_language = models.CharField(max_length=100, null=True, blank=True)
    # additional fields as needed

    def __str__(self):
        return self.name + "-" + self.university.name


class Fee(models.Model):
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12,default=0.00, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.amount})"


class UniversityQuestion(models.Model):
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    question = models.TextField()


class UniversityAIWeight(models.Model):
    university_profile = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    gpa_weight = models.FloatField(default=1.0)
    sports_interest_weight = models.FloatField(default=1.0)
    extracurricular_interest_weight = models.FloatField(default=1.0)

    def __str__(self):
        return self.university_profile.name + "Score Weight"

