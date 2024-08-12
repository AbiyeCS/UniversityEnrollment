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
