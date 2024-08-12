from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'required': 'Please enter the Username'}, widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control form-control-xl',}))
    password = forms.CharField(error_messages={'required': 'Please enter the password'}, widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control form-control-xl',}))


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].widget.attrs['class'] = 'form-control'