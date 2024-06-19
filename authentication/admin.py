from django.contrib import admin
from .models import *

from django.apps import apps
models = apps.get_models()
# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_type")


admin.site.register(UserProfile, UserProfileAdmin)

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass