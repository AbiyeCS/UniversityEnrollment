from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout as Logout_user
from django.contrib.auth import login as Login_user
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import *
from .models import *
from student_panel.models import StudentProfile
from university_panel.models import UniversityProfile
from django.views.decorators.cache import cache_control


def home(request):
    return redirect('login_user')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    InvalidDetails = None
    user_auth = None

    form = LoginForm()
    if request.user.is_authenticated:
        # check user type and redirect
        if request.user.is_staff:
            return HttpResponseRedirect('/admin_dashboard/')
        if request.user.userprofile.user_type == 'student':
            return HttpResponseRedirect('/student/dashboard/')
        if request.user.userprofile.user_type == 'university':
            return HttpResponseRedirect('/university/dashboard/')
    return_url = request.GET.get('next', None)

    print(request.POST)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if return_url:
                return HttpResponseRedirect(return_url)
            if request.user.is_staff:
                return HttpResponseRedirect('/admin_dashboard/')
            if request.user.userprofile.user_type == 'student':
                return HttpResponseRedirect('/student/dashboard/')
            if request.user.userprofile.user_type == 'university':
                return HttpResponseRedirect('/university/dashboard/')
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            if "@" in username:
                print(username)
                try:
                    user_obj = User.objects.get(email=username)
                    print(user_obj)
                    if user_obj.check_password(password):
                        print(user_obj)
                        user_auth = authenticate(username=user_obj.username, password=password)
                    else:
                        InvalidDetails = "Please Enter Correct Email/Password"
                except Exception as e:
                    print(e)
                    InvalidDetails = "Please Enter Correct Email/Password"
            else:
                user_auth = authenticate(username=username, password=password)
                if not user_auth:
                    InvalidDetails = "Please Enter Correct Username/Password"
            if not InvalidDetails and user_auth:
                print("user login")
                Login_user(request, user_auth)
                messages.success(request, 'User Logged In Successfully')
                if request.user.is_staff:
                    return HttpResponseRedirect('/admin_dashboard/')
                if request.user.userprofile.user_type == 'student':
                    return HttpResponseRedirect('/student/dashboard/')
                if request.user.userprofile.user_type == 'university':
                    return HttpResponseRedirect('/university/dashboard/')
                else:
                    messages.error(request, "only students/university can login right now")
                    return redirect('login_user')
            else:
                messages.error(request, 'Invalid login credentials. Please check your username and password.')
        else:
            print("form not valid")
    return render(request, 'authentication/login.html', {
        'form': form,
        'InvalidDetails': InvalidDetails,
    })


def logout_user(request):
    print('in this view')
    Logout_user(request)
    messages.info(request, 'User has been Log out')
    return redirect('login_user')


def register(request):
    errors = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid():
            print("in form valid")
            user = form.save()
            user_type = request.POST.get('user_type')
            user_profile = UserProfile.objects.create(user=user, user_type=user_type)
            Login_user(request, user)
            if request.user.userprofile.user_type == 'student':
                StudentProfile.objects.create(user_profile=user_profile)
                return HttpResponseRedirect('/student/dashboard/')
            if request.user.userprofile.user_type == 'university':
                uni_name = request.POST.get('uni_name')
                uni_address = request.POST.get('uni_address')
                UniversityProfile.objects.create(user_profile=user_profile, name=uni_name, address=uni_address)
                return HttpResponseRedirect('/university/dashboard/')
            else:
                messages.error(request, "only students/university can login right now")
                return redirect('login_user')
        else:
            print("user form", form.errors)
            print(profile_form.errors)
            errors = form.errors
    else:
        form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'authentication/register.html',
                  {'form': form, 'profile_form': profile_form, 'errors': errors})


def access_denied(request):
    return render(request, 'authentication/access_denied.html')
