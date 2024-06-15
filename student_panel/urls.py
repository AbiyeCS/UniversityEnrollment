from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name="student_dashboard"),
    path('application_create/<int:course_id>/', views.application_create, name='application_create'),
    path('application_list/', views.application_list, name='application_list'),
    path('university_lists/', views.university_lists, name='university_lists'),
    path('university_detail/<int:uni_id>/', views.university_detail, name='university_detail'),
    path('add_educational_background/', views.add_educational_background, name='add_educational_background'),
    path('delete_educational_background/<int:id>/', views.delete_educational_background, name='delete_educational_background'),

    path('courses_lists/', views.courses_lists, name='courses_lists'),
    path('courses_detail/<int:course_id>/', views.courses_detail, name='courses_detail'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('faq/', views.faq, name='faq'),
]
