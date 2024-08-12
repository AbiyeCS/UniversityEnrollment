from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login_user"),
    path('logout/', views.logout_user, name="logout_user"),
    path('register/', views.register, name="register"),
    path('access_denied/', views.access_denied, name="access_denied"),
]
