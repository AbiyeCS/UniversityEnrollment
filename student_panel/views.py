import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from university_panel.models import UniversityProfile, Course, UniversityQuestion
from .forms import *
# Create your views here.
from .models import ApplicationQA, FAQ, Subject, ChatMessage
from authentication.permissions import user_type_required


@user_type_required('student')
def student_dashboard(request):
    universities = UniversityProfile.objects.all()
    total_number_uni = UniversityProfile.objects.all().count()
    total_courses = Course.objects.all().count()
    total_application = Application.objects.filter(student=request.user.userprofile.studentprofile).count()
    total_review = Application.objects.filter(student=request.user.userprofile.studentprofile).exclude(status='pending').count()

    context = {
        "total_number_uni": total_number_uni,
        "total_courses": total_courses,
        "total_application": total_application,
        "total_review": total_review,
        "featured_universities":universities
    }
    return render(request, 'student_panel/index.html', context)


@user_type_required('student')
def university_lists(request):
    universities = UniversityProfile.objects.all()
    context = {
        "universities":universities
    }
    return render(request,'student_panel/university_list.html',context)


@user_type_required('student')
def university_detail(request, uni_id):
    university = UniversityProfile.objects.get(id=uni_id)
    courses_list = Course.objects.filter(university=university)
    context = {
        "university":university,
        "courses_list":courses_list
    }
    return render(request,'student_panel/university_detail.html',context)


@user_type_required('student')
def courses_lists(request):
    courses = Course.objects.all()
    context = {
        "courses":courses
    }
    return render(request,'student_panel/courses_list.html',context)


@user_type_required('student')
def courses_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {
        "course":course
    }
    return render(request,'student_panel/course_details.html',context)


@user_type_required('student')
def application_list(request):
    try:
        application_object_list = Application.objects.filter(student=request.user.userprofile.studentprofile)
    except Exception as e:
        print(e)
        application_object_list = []
    context = {
        "application_object_list":application_object_list
    }
    return render(request,'student_panel/applications_list.html', context)


@user_type_required('student')
def application_create(request, course_id):
    course_obj = Course.objects.get(id=course_id)
    university = course_obj.university
    student_profile, stud_created = StudentProfile.objects.get_or_create(user_profile=request.user.userprofile)
    application_object, app_created = Application.objects.get_or_create(university=university,student=student_profile, course=course_obj)
    application_answers = ApplicationQA.objects.filter(application=application_object)
    university_questions = UniversityQuestion.objects.filter(university=university)
    educational_backgrounds = EducationalBackground.objects.filter(student_profile=student_profile)
    print(request.POST)
    if request.POST:
        personal_statement = request.POST.get('personal_statement')
        question_ids = request.POST.getlist('question_ids')
        application_id = request.POST.get('application_id')
        application_object_post = Application.objects.get(id=application_id)

        if question_ids:
            for question_id in question_ids:
                student_answer = request.POST.get(f'university_question_{question_id}')
                university_question = UniversityQuestion.objects.get(id=question_id)
                student_answer_obj, ans_created = ApplicationQA.objects.get_or_create(application=application_object_post, question=university_question.question)
                student_answer_obj.answer = student_answer
                student_answer_obj.save()
        print(application_object_post,'obj')
        application_object_post.personal_statement = personal_statement
        application_object_post.save()
        messages.success(request,'Successfully updated')
        return redirect('application_list')

    return render(request, 'student_panel/create_application.html', {
        'university': university,
        'course_obj': course_obj,
        'university_questions':university_questions,
        'application_object':application_object,
        'student_profile':student_profile,
        'educational_backgrounds':educational_backgrounds,
        'application_answers':application_answers,

    })


@user_type_required('student')
def student_profile(request):
    student_profile, created = StudentProfile.objects.get_or_create(user_profile=request.user.userprofile)
    educational_backgrounds = EducationalBackground.objects.filter(student_profile=student_profile)
    user = request.user
    if request.POST:
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        interested_in_sports = 'interested_in_sports' in request.POST
        interested_sport_name = request.POST.get('interested_sport_name', 'na')
        interested_sport_certification = 'interested_sport_certification' in request.POST
        interested_sport_description = request.POST.get('interested_sport_description', '')

        interested_in_extracurricular = 'interested_in_extracurricular' in request.POST
        interested_extracurricular_name = request.POST.get('interested_extracurricular_name', 'na')
        interested_extracurricular_certification = 'interested_extracurricular_certification' in request.POST
        interested_extracurricular_description = request.POST.get('interested_extracurricular_description', '')

        if first_name and first_name != '':
            user.first_name = first_name
        if last_name and last_name != '':
            user.last_name = last_name
        if date_of_birth and date_of_birth != '':
            student_profile.date_of_birth = date_of_birth
        if address and address != '':
            student_profile.address = address
        if phone_number and phone_number != '':
            student_profile.phone_number = phone_number

        student_profile.interested_in_sports = interested_in_sports
        student_profile.interested_sport_name = interested_sport_name
        student_profile.interested_sport_certification = interested_sport_certification
        student_profile.interested_sport_description = interested_sport_description

        student_profile.interested_in_extracurci = interested_in_extracurricular
        student_profile.interested_extracurci_name = interested_extracurricular_name
        student_profile.interested_extracurci_certification = interested_extracurricular_certification
        student_profile.interested_extracurci_description = interested_extracurricular_description
        student_profile.save()
        student_profile.calculate_sports_interest_score()
        student_profile.calculate_extracurricular_interest_score()
        student_profile.calculate_overall_educational_score()
        user.save()
        return redirect('student_profile')
    context = {
        'student_profile':student_profile,
        'educational_backgrounds':educational_backgrounds
    }
    return render(request, 'student_panel/student_profile.html', context)


@user_type_required('student')
def faq(request):
    faq = FAQ.objects.filter(title='student').first()
    context = {
        "faq":faq
    }
    return render(request, 'student_panel/faq.html' ,context)



@user_type_required('student')
def add_educational_background(request):
    if request.method == 'POST':
        form = EducationalBackgroundForm(request.POST)
        if form.is_valid():
            student_profile_id = request.POST.get('student_profile_id')
            student_profile_object = StudentProfile.objects.get(id=student_profile_id)
            educational_background = form.save(commit=False)
            educational_background.student_profile = student_profile_object
            educational_background.save()

            subjects_data = json.loads(request.POST.get('subjects', '[]'))
            subjects = []
            for subject_data in subjects_data:
                subject = Subject.objects.create(
                    title=subject_data.get('title'),
                    element_code=subject_data.get('element_code'),
                    grade=subject_data.get('grade')
                )
                subjects.append(subject)
                educational_background.subject_list.add(subject)

            data = {
                'id': educational_background.id,
                'institution_name': educational_background.institution_name,
                'degree_name': educational_background.degree_name,
                'degree_level': educational_background.get_degree_level_display(),
                'total_marks': educational_background.total_marks,
                'obtained_marks': educational_background.obtained_marks,
                'grade': educational_background.grade,
                'obtained_cgpa': educational_background.obtained_cgpa,
                'total_cgpa': educational_background.total_cgpa,
                'percentage': educational_background.percentage,
                'attended_from': educational_background.attended_from,
                'attended_to': educational_background.attended_to,
                'subjects': [{'title': s.title, 'grade': s.grade} for s in subjects],
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid form'}, status=400)


@user_type_required('student')
def delete_educational_background(request, id):
    educational_background = get_object_or_404(EducationalBackground, pk=id)
    educational_background.delete()
    return JsonResponse({'id': id})


@login_required(login_url='/login/')
def support(request):
    current_user = request.user
    received_messages = ChatMessage.objects.filter(receiver=current_user).values('sender').distinct()
    senders = User.objects.filter(id__in=[msg['sender'] for msg in received_messages])
    all_users = User.objects.all()
    context = {
        'senders': senders,
        'all_users': all_users
    }
    return render(request, 'student_panel/support.html', context)


@login_required(login_url='/login/')
def chat_message_room(request, user_id):
    current_user = request.user
    other_user = get_object_or_404(User, id=user_id)
    new_messages = ChatMessage.objects.filter(
        (Q(receiver=current_user) & Q(sender=other_user)) |
        (Q(receiver=other_user) & Q(sender=current_user))
    ).order_by('created_at')

    context = {
        'other_user': other_user,
        'messages': new_messages
    }
    return render(request, 'chat_messages/chat_message_room.html', context)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        receiver_id = data['receiver_id']
        message_text = data['message']
        receiver = get_object_or_404(User, id=receiver_id)
        ChatMessage.objects.create(receiver=receiver, sender=request.user, message=message_text)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})

