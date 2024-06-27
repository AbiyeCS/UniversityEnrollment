from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .forms import CourseForm, UniversityQuestionForm, UniversityProfileForm, WeightageForm
from student_panel.models import *
from authentication.permissions import user_type_required
from aiadmin.ai_utils import load_model, create_feedback_entry
import numpy as np
import pandas as pd


# Create your views here.

def customize_weights_view(request):
    university_profile = request.user.userprofile.universityprofile
    university_ai_weight, created = UniversityAIWeight.objects.get_or_create(university_profile=university_profile)
    if request.method == 'POST':
        form = WeightageForm(request.POST, instance=university_ai_weight)
        if form.is_valid():
            form.save()
            return redirect('ai_recommendations')
    else:
        form = WeightageForm(instance=university_ai_weight)
    return render(request, 'university_panel/customize_weights.html', {'form': form})



@user_type_required('university')
def university_dashboard(request):
    model = load_model()
    university = request.user.userprofile.universityprofile
    university_weight = UniversityAIWeight.objects.filter(university_profile=university).first()
    accepted_application = Application.objects.filter(university=university, status='accepted').count()
    total_courses = Course.objects.filter(university=university).count()
    total_application = Application.objects.filter(university=university).count()
    total_review = Application.objects.filter(university=university).exclude(status='pending').count()

    recommendations = {}
    try:
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
            top_5_applications = [applications[int(i)] for i in top_5_indices]
            print("top_5_applications", top_5_applications)
            recommendations = top_5_applications
    except Exception as e:
        print(e)
    context = {
        "accepted_application": accepted_application,
        "total_courses": total_courses,
        "total_application": total_application,
        "total_review": total_review,
        "apps": recommendations,
        "university_weight":university_weight,
    }
    return render(request,"university_panel/index.html", context)


@user_type_required('university')
def uni_application_list(request):
    university_profile = request.user.userprofile.universityprofile
    application_object_list = Application.objects.filter(university=university_profile)

    context = {
        "application_object_list":application_object_list
    }
    return render(request,"university_panel/uni_application_list.html", context)


@user_type_required('university')
def uni_application_review(request, application_id):
    application_object = get_object_or_404(Application, id=application_id)
    educational_backgrounds = EducationalBackground.objects.filter(student_profile=application_object.student)
    question_answer_object = ApplicationQA.objects.filter(application = application_object)
    all_notes = ApplicationNote.objects.filter(application=application_object)
    print(request.POST, "request post")
    if 'note' in request.POST:
        note = request.POST.get('note')
        if application_object and note:
            ApplicationNote.objects.create(note=note,application=application_object)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if 'new_status' in request.POST:
        new_status = request.POST.get('new_status')
        if application_object:
            application_object.status = new_status
            application_object.save()
            if new_status == 'accepted':
                create_feedback_entry(application_object,1)
            if new_status == 'rejected':
                create_feedback_entry(application_object,0)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



    context = {
        "application_object" : application_object,
        "educational_backgrounds":educational_backgrounds,
        "question_answer_object":question_answer_object,
        "all_notes":all_notes

    }
    return render(request,"university_panel/uni_application_review.html", context)


@user_type_required('university')
def uni_course_list(request):
    print(request.user.userprofile, )
    university_profile = request.user.userprofile.universityprofile
    all_courses = Course.objects.filter(university=university_profile)
    all_disciplines = Discipline.objects.all()
    all_fees = Fee.objects.filter(university=university_profile)
    all_questions = UniversityQuestion.objects.filter(university=university_profile)
    print(request.POST)
    if 'fee_amount' in request.POST:
        fee_name = request.POST.get('fee_name')
        fee_amount = request.POST.get('fee_amount')
        if fee_name and fee_amount:
            Fee.objects.create(name=fee_name, amount=fee_amount,university=university_profile)
            return redirect('uni_course_list')


    context = {
        'all_courses':all_courses,
        'all_disciplines':all_disciplines,
        'all_fees':all_fees,
        'university_profile':university_profile,
        'all_questions':all_questions,
    }
    return render(request,"university_panel/course_list.html", context)


@user_type_required('university')
def create_question(request):
    if request.method == 'POST':
        form = UniversityQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.university = request.user.userprofile.universityprofile
            question.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UniversityQuestionForm()
        return render(request, 'university_panel/question-form.html', {'form': form})


@user_type_required('university')
def edit_question(request, question_id):
    question = get_object_or_404(UniversityQuestion, id=question_id)
    if request.method == 'POST':
        form = UniversityQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UniversityQuestionForm(instance=question)
        return render(request, 'university_panel/question-form.html', {'form': form})


@user_type_required('university')
def delete_question(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(UniversityQuestion, id=question_id)
        question.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@user_type_required('university')
def create_course(request, university_id):
    print(university_id)
    university = get_object_or_404(UniversityProfile, id=university_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, university=university)
        if form.is_valid():
            course = form.save(commit=False)
            course.university = university
            course.save()
            form.save_m2m()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CourseForm(university=university)
    return render(request, 'university_panel/course_form.html', {'form': form, 'university': university})


@user_type_required('university')
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    university = course.university
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course, university=university)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CourseForm(instance=course, university=university)
    return render(request, 'university_panel/course_form.html', {'form': form, 'university': university})


@user_type_required('university')
def delete_course(request, course_id):
    if request.method == 'POST':
        try:
            course = get_object_or_404(Course, id=course_id)
            course.delete()
            return JsonResponse({'success': True})
        except Course.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Course not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@user_type_required('university')
def uni_profile(request):
    university_profile = request.user.userprofile.universityprofile
    university_weight = UniversityAIWeight.objects.get(university_profile=university_profile)
    if request.method == 'POST':
        print(request.POST)
        form = UniversityProfileForm(request.POST, request.FILES, instance=university_profile)
        gpa_weight = request.POST.get('gpa_weight')
        sports_interest_weight = request.POST.get('sports_interest_weight')
        extracurricular_interest_weight = request.POST.get('extracurricular_interest_weight')
        if form.is_valid():
            form.save()
            if gpa_weight and sports_interest_weight and extracurricular_interest_weight:
                university_weight.gpa_weight = gpa_weight
                university_weight.sports_interest_weight = sports_interest_weight
                university_weight.extracurricular_interest_weight = extracurricular_interest_weight
                university_weight.save()
            messages.success(request,"Updated Successfully")
            return redirect('uni_profile')
    else:
        form = UniversityProfileForm(instance=university_profile)

    context = {
        'form': form,
        'university_profile': university_profile,
        'university_weight':university_weight,
    }

    return render(request,"university_panel/uni_profile.html", context)


@user_type_required('university')
def uni_faq(request):
    return render(request,"university_panel/uni_faq.html")


@user_type_required('university')
def uni_support(request):
    return render(request,"university_panel/uni_support.html")


@csrf_exempt
@require_POST
def toggle_flag(request):
    application_id = request.POST.get('application_id')
    application = Application.objects.get(id=application_id)
    application.is_flagged = not application.is_flagged
    application.save()
    return JsonResponse({'is_flagged': application.is_flagged})









