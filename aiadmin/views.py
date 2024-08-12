import csv
import json

import numpy as np
import pandas as pd
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from aiadmin.models import FeedbackModel
from student_panel.models import Application
from university_panel.models import UniversityAIWeight
from .ai_utils import load_model
from .forms import *
from .tasks import process_training_file


def admin_dashboard(request):
    total_number_uni = UniversityProfile.objects.all().count()
    total_courses = Course.objects.all().count()
    total_application = Application.objects.all().count()
    total_review = Application.objects.all().exclude(status='pending').count()
    context = {
        "total_number_uni": total_number_uni,
        "total_courses": total_courses,
        "total_application": total_application,
        "total_review": total_review,
    }
    return render(request, 'aiadmin/index.html', context)


def ai_recommendations(request):
    model = load_model()
    universities = UniversityProfile.objects.all()
    recommendations = {}

    for university in universities:
        try:
            print(university)
            university_weights = UniversityAIWeight.objects.get(university_profile=university)
            applications = Application.objects.filter(university=university, status='pending')
            data = []
            for app in applications:
                student = app.student
                row = {
                    'gpa_score': student.education_gpa_score if student.education_gpa_score else 0,
                    'sports_interest_score': student.sports_interest_score if student.sports_interest_score else 0,
                    'extracurricular_interest_score': student.extracurricular_interest_score if student.extracurricular_interest_score else 0,
                    'uni_gpa_weight': university_weights.gpa_weight,
                    'uni_sports_weight': university_weights.sports_interest_weight,
                    'uni_extracurricular_weight': university_weights.extracurricular_interest_weight,
                }
                print(row)
                data.append(row)
            df = pd.DataFrame(data)
            print(df)
            if not df.empty:
                predictions = model.predict_proba(df)[:, 1]
                sorted_indices = np.argsort(predictions)[::-1]
                top_5_indices = sorted_indices[:5]
                print("top_5_indices", top_5_indices)
                top_5_applications = [applications[int(i)] for i in top_5_indices]  # Convert int64 to int
                print("top_5_applications", top_5_applications)
                recommendations[university] = top_5_applications
        except Exception as e:
            print(e)

    context = {'recommendations': recommendations}
    return render(request, 'aiadmin/ai_recommendations.html', context)


def model_training_view(request):
    if request.method == 'POST':
        form = TrainingFileForm(request.POST, request.FILES)
        if form.is_valid():
            training_file = form.save()
            process_training_file.delay(training_file.id)
            messages.success(request, 'File uploaded successfully and training started.')
            return redirect('model_training')
    else:
        form = TrainingFileForm()

    # Handle GET request
    trained_model_list = TrainingModel.objects.all().order_by('-uploaded_at')

    return render(request, 'aiadmin/model_training.html', {'form': form, 'trained_model_list': trained_model_list})


def training_data(request):
    training_data_objects = FeedbackModel.objects.all().order_by('created_at')
    if request.POST:
        print(request.POST)
        gpa_score = request.POST.get('gpa_score')
        sports_interest_score = request.POST.get('sports_interest_score')
        extracurricular_interest_score = request.POST.get('extracurricular_interest_score')
        uni_gpa_weight = request.POST.get('uni_gpa_weight')
        uni_sports_weight = request.POST.get('uni_sports_weight')
        uni_extracurricular_weight = request.POST.get('uni_extracurricular_weight')
        accepted = request.POST.get('accepted')
        FeedbackModel.objects.create(gpa_score=gpa_score, sports_interest_score=sports_interest_score,
                                     extracurricular_interest_score=extracurricular_interest_score,
                                     uni_gpa_weight=uni_gpa_weight, uni_sports_weight=uni_sports_weight,
                                     uni_extracurricular_weight=uni_extracurricular_weight, accepted=accepted)
        messages.success(request, "Data Added Successfully")
        return redirect('training_data')

    context = {
        "training_data_objects": training_data_objects
    }
    return render(request, "aiadmin/training_data.html", context)


def delete_data(request, id):
    FeedbackModel.objects.get(id=id).delete()
    messages.success(request, "Data Deleted Successfully")
    return redirect('training_data')


def clean_data(request):
    FeedbackModel.objects.all().delete()
    messages.success(request, "All Data Cleaned Successfully")
    return redirect('training_data')


def download_data(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="training_data.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['gpa_score', 'sports_interest_score', 'extracurricular_interest_score', 'uni_gpa_weight', 'uni_sports_weight',
         'uni_extracurricular_weight', 'accepted'])

    for data in FeedbackModel.objects.all():
        writer.writerow([data.gpa_score, data.sports_interest_score, data.extracurricular_interest_score,
                         data.uni_gpa_weight, data.uni_sports_weight, data.uni_extracurricular_weight,
                         1 if data.accepted else 0])

    return response


def dislike_recommendation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        app_id = data.get('app_id')
        try:
            app = Application.objects.get(id=app_id)
            university_weights = UniversityAIWeight.objects.get(university_profile=app.university)
            FeedbackModel.objects.create(
                gpa_score=app.student.education_gpa_score or 0,
                sports_interest_score=app.student.sports_interest_score or 0,
                extracurricular_interest_score=app.student.extracurricular_interest_score or 0,
                uni_gpa_weight=university_weights.gpa_weight,
                uni_sports_weight=university_weights.sports_interest_weight,
                uni_extracurricular_weight=university_weights.extracurricular_interest_weight,
                accepted=0
            )
            return JsonResponse({'status': 'success'})
        except Application.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Application not found.'})
        except UniversityAIWeight.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'University weights not found.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


# cruds for University , student , pplication and courses
class UniversityProfileListView(ListView):
    model = UniversityProfile
    template_name = 'aiadmin/university_profile_list.html'
    context_object_name = 'universities'


class UniversityProfileCreateView(CreateView):
    model = UniversityProfile
    form_class = UniversityProfileForm
    template_name = 'aiadmin/university_profile_form.html'
    success_url = reverse_lazy('university_profile_list')


class UniversityProfileUpdateView(UpdateView):
    model = UniversityProfile
    form_class = UniversityProfileForm
    template_name = 'aiadmin/university_profile_form.html'
    success_url = reverse_lazy('university_profile_list')


class UniversityProfileDeleteView(DeleteView):
    model = UniversityProfile
    template_name = 'aiadmin/university_profile_confirm_delete.html'
    success_url = reverse_lazy('university_profile_list')


# Course views
class CourseListView(ListView):
    model = Course
    template_name = 'aiadmin/course_list.html'
    context_object_name = 'courses'


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'aiadmin/course_form.html'
    success_url = reverse_lazy('course_list')


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'aiadmin/course_form.html'
    success_url = reverse_lazy('course_list')


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'aiadmin/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')
