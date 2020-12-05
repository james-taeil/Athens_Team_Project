from django.urls import path
from mainpage import views


urlpatterns = [
    path('', views.mainpage),
    path('online/', views.mainpage_select_lecture),
    path('online/<int:pk>', views.mainpage_select_online_index_teacher),
    path('online/content/<int:pk>',views.mainpage_online_contents),
    path('agree2/', views.mainagree2),
    path('agree1/', views.mainagree1),
    # 동현
    path('zx/', views.faq_list, name = 'faq_list'),
    path('intd/', views.teacher_list, name = 'teacher_list'),
    path('notice/', views.notice_list, name = 'notice_list'),
    path('notice2/<int:notice_no>', views.notice_list2, name = 'notice_list2'),


]

