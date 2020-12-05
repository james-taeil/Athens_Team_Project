from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

app_name = 'admin'

urlpatterns = [
    # ------------------------------ 민우
    # 메인화면
    path('', views.index, name='index'),
    # 재직 선생님
    path('teacher.in', views.teacher_in, name='teacherin'),
    # 퇴원 선생님
    path('teacher.out', views.teacher_out, name='teacherout'),
    # 선생님 상세
    path('teacher_detail/<int:teacher_tbl_t_no>', views.teacher_detail, name='teacher_detail'),
    # 재원생 목록
    path('student.in', views.student_in, name='studentin'),
    # 퇴원생 목록
    path('student.out', views.student_out, name='studentout'),
    # 학생 상세
    path('student_detail/<int:c_no>', views.student_detail, name='student_detail'),
    # 강의 등록
    path('lecture', views.lecture_create, name='lecture_create'),
    # 학부모 목록
    path('parents_list', views.parents_list, name='parents_list'),
    # 로그인(관리자)
    path('login', views.login_admin, name='login_admin'),
    # 로그아웃(관리자)
    path('logout', views.logout_admin, name='logout_admin'),
    # 상담 목록
    path('consult_list', views.consult_list, name='consult_list'),
    # 사용자 페이지 관리
    path('userpage', views.userpage, name='userpage'),
    # 차트 데이터 json(선생님 통계)
    path('chart.data/', views.chart_data, name='chart_data'),
    # 학생,학부모 통계
    path('chart.customer.data/', views.chart_customer_data, name='chart_customer_data'),
    # url(r'^chart.data$', views.chart_data, name = 'chart_data'),
    path('profile/', views.profile, name='profile'),
    # 프로필 사진 변경
    path('profile/<int:t_no>', views.profile_picture, name='profile_picture'),
    #-----------------------------------------------------병훈
    path('notice', views.notice, name='notice'),
    path('faq', views.faq, name='faq'),
    path('noticelist', views.noticelist, name='noticelist'),
    path('noticedetail/<int:notice_tbl_t_no>', views.noticedetail, name='noticedetail'),
    path('noticemodify/<int:notice_tbl_t_no>', views.noticemodify, name='noticemodify'),
    path('faqlist', views.faqlist, name='faqlist'),
    path('payment', views.payment, name='payment'),
    path('faqdetail/<int:faq_tbl_t_no>', views.faqdetail, name='faqdetail'),
    path('faqmodify/<int:faq_tbl_t_no>', views.faqmodify, name='faqmodify'),
    # 강의 등록
    path('lecturelist', views.lecturelist, name='lceturelist'),
    path('lecturemodify/<int:lecture_tbl_l_no>', views.lecturemodify, name='lecturemodify'),
    path('lecturemodify2/<int:lecture_tbl_l_no>', views.lecturemodify2, name='lecturemodify2'),



]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)