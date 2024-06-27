from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.university_dashboard, name="university_dashboard"),
    path('uni_application_list/', views.uni_application_list, name="uni_application_list"),
    path('uni_application_review/<int:application_id>/', views.uni_application_review, name="uni_application_review"),
    path('uni_course_list/', views.uni_course_list, name="uni_course_list"),
    path('create_question/', views.create_question, name='create_question'),
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),

    path('create_course/<int:university_id>/', views.create_course, name='create_course'),
    path('edit_course/<int:pk>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('uni_faq/', views.uni_faq, name="uni_faq"),
    path('uni_support/', views.uni_support, name="uni_support"),
    path('uni_profile/', views.uni_profile, name="uni_profile"),
    path('toggle_flag/', views.toggle_flag, name='toggle_flag'),

]
