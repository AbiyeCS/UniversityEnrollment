from django import forms
from .models import Course, Fee, UniversityQuestion, UniversityProfile, UniversityAIWeight

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'short_description', 'discipline', 'fee', 'requirements', 'university_course_url', 'taught_language']
        widgets = {
            'discipline': forms.CheckboxSelectMultiple,
            'fee': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        university = kwargs.pop('university', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxSelectMultiple)):
                field.widget.attrs['class'] = 'form-control'
        if university:
            self.fields['fee'].queryset = Fee.objects.filter(university=university)


class UniversityQuestionForm(forms.ModelForm):
    class Meta:
        model = UniversityQuestion
        fields = ['question']


    def __init__(self, *args, **kwargs):
        university = kwargs.pop('university', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



class UniversityProfileForm(forms.ModelForm):
    class Meta:
        model = UniversityProfile
        fields = ['name', 'address', 'display_image','display_image_file', 'site_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'display_image': forms.TextInput(attrs={'class': 'form-control'}),
            'display_image_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'site_url': forms.URLInput(attrs={'class': 'form-control'}),
        }



class WeightageForm(forms.ModelForm):
    class Meta:
        model = UniversityAIWeight
        fields = ['gpa_weight', 'sports_interest_weight', 'extracurricular_interest_weight']



