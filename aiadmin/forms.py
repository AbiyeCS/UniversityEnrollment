from django import forms

from university_panel.models import UniversityProfile, Course
from .models import TrainingModel

class TrainingFileForm(forms.ModelForm):
    class Meta:
        model = TrainingModel
        fields = ['file']


class UniversityProfileForm(forms.ModelForm):
    class Meta:
        model = UniversityProfile
        fields = [
            'user_profile', 'name', 'address', 'display_image', 'display_image_file', 'site_url'
        ]
    def __init__(self, *args, **kwargs):
        super(UniversityProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'university', 'name', 'short_description', 'discipline', 'fee', 'requirements', 'university_course_url', 'taught_language'
        ]

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

