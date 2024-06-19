from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('university', 'University'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.user.username + "-" + self.user_type

    def is_university(self):
        if self.user_type == 'university':
            return True
        return False

#
# class AdminProfile(models.Model):
#     user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
#     # additional fields as needed
