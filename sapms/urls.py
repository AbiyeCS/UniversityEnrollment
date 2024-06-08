"""
URL configuration for sapms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from student_panel.views import chat_message_room, support, send_message
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('student/', include('student_panel.urls')),
    path('university/', include('university_panel.urls')),
    path('admin_dashboard/', include('aiadmin.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('support/', support, name='support'),
    path('chat/<int:user_id>/', chat_message_room, name='chat_room'),
    path('send_message/', send_message, name='send_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
