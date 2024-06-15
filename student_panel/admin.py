from django.contrib import admin

# Register your models here.

from django.apps import apps
models = apps.get_models()
# Register your models here.
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass