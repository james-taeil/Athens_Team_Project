from django.urls import path
from . import views

app_nap = 'exam'

urlpatterns = [

    path('lecture_select/', views.lecture_select ,name='lecture_select'),
    path('<int:l_no>/', views.exam_enroll, name='exam_enroll'),
    path('<int:l_no>/<int:te_no>/', views.exam_modify, name='exam_modify'),
    path('<int:l_no>/enrollment/', views.enrollment, name='enrollment'),
    path('lecture_list/', views.test_lecture_list, name='test_lecture_list'),
]