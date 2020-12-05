from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name='manage'

urlpatterns = [
    path('teacher/manage/',select_lecture_teacher),
    path('teacher/manage/<int:pk>',student_info_manage),
    path('teacher/manage/score/<int:pk>',look_up_score),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)