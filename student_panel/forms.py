from django import forms

from .models import EducationalBackground


class EducationalBackgroundForm(forms.ModelForm):
    class Meta:
        model = EducationalBackground
        fields = '__all__'