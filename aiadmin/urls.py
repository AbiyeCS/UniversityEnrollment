from django.urls import path
from . import views
from .views import (
    UniversityProfileListView, UniversityProfileCreateView, UniversityProfileUpdateView, UniversityProfileDeleteView,
    CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView
)


urlpatterns = [
    path('', views.admin_dashboard, name="admin_dashboard"),
    path('all_recommendations/', views.ai_recommendations, name="ai_recommendations"),
    path('model-training/', views.model_training_view, name='model_training'),
    path('training-data/', views.training_data, name='training_data'),
    path('delete-data/<int:id>/', views.delete_data, name='delete_data'),
    path('clean-data/', views.clean_data, name='clean_data'),
    path('download-data/', views.download_data, name='download_data'),
    path('dislike-recommendation/', views.dislike_recommendation, name='dislike_recommendation'),
    #
    path('universities/', UniversityProfileListView.as_view(), name='university_profile_list'),
    path('universities/add/', UniversityProfileCreateView.as_view(), name='university_profile_add'),
    path('universities/edit/<int:pk>/', UniversityProfileUpdateView.as_view(), name='university_profile_edit'),
    path('universities/delete/<int:pk>/', UniversityProfileDeleteView.as_view(), name='university_profile_delete'),
    path('courses/', CourseListView.as_view(), name='admin_course_list'),
    path('courses/add/', CourseCreateView.as_view(), name='course_add'),
    path('courses/edit/<int:pk>/', CourseUpdateView.as_view(), name='course_edit'),
    path('courses/delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),

]
