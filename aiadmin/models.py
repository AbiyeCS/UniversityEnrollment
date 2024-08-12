from django.db import models

# Create your models here.
class TrainingModel(models.Model):
    file = models.FileField(upload_to='training_files/', null=True, blank=True)
    model_path = models.CharField(max_length=255, null=True, blank=True)
    accuracy = models.CharField(max_length=50, null=True,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_model_path(self):
        if self.model_path:
            return self.model_path.split('UniversityEnrollment')[1]
        else:
            return ""


class FeedbackModel(models.Model):
    gpa_score = models.DecimalField(max_digits=5,decimal_places=2)
    sports_interest_score = models.DecimalField(max_digits=5,decimal_places=2)
    extracurricular_interest_score = models.DecimalField(max_digits=5,decimal_places=2)
    uni_gpa_weight = models.DecimalField(max_digits=5,decimal_places=2)
    uni_sports_weight = models.DecimalField(max_digits=5,decimal_places=2)
    uni_extracurricular_weight = models.DecimalField(max_digits=5,decimal_places=2)
    accepted = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

