from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.utils import timezone
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from django.contrib import messages

# 프로필
@user_passes_test(lambda u: u.is_superuser, login_url='admin:login_admin')
def profile(request):
    # 관리자에 해당하는 teacher_tbl의 객체를 불러옴
    user = teacher_tbl.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        print(request.user.id)
        # 관리자와 맞는 teacher_tbl의 객체를 불러온다
        try:
            try:
                teacher =teacher_tbl.objects.get(user_id=request.user.id)
                teacher.t_name = request.POST['name']
                teacher.t_phone = request.POST['phone']
                teacher.t_gender = request.POST['gender']
                teacher.t_subject = request.POST['subject']
                # teacher.t_birth = request.POST['birth']
                teacher.t_add = request.POST['add']
                # teacher.t_file = request.FILES['img']
                teacher.t_subject = request.POST['subject']
                teacher.t_state = True
                teacher.save()
                # user 테이블 email속성에 이메일 저장
                user_info = User.objects.get(id=teacher.user_id)
                user_info.email = request.POST['email']
                user_info.first_name = teacher.t_file
                user_info.save()
                # 모든 정보를 제대로 입력했을 경우 회원 정보가 저장되었다는 알람창을 띄운다.

                return HttpResponse('<script type="text/javascript"> alert("회원 정보가 저장되었습니다."); location.href = "/admin";</script>')

                #입력되지 않은 값이 있을 시 알람창을 띄우고 다시 전 화면으로 돌아간다.
            except:
                return HttpResponse('<script type="text/javascript"> alert("모든 정보를 입력 해 주세요"); history.back();</script>' )
        # 만약 불러오지 못한다면(등록되어있지 않다면) 새로 등록해준다.
        except:
            teacher = teacher_tbl.objects.create(user_id=request.user.id)
            teacher.t_name = request.POST['name']
            teacher.t_phone = request.POST['phone']
            teacher.t_gender = request.POST['gender']
            teacher.t_subject = request.POST['subject']
            # teacher.t_birth = request.POST['birth']
            teacher.t_add = request.POST['add']
            teacher.t_file = request.FILES['img']
            teacher.t_subject = request.POST['subject']
            teacher.t_state = True
            teacher.save()
            # user 테이블 email속성에 이메일 저장
            user_info = User.objects.get(id = teacher.user_id)
            user_info.email = request.POST['email']
            user_info.first_name = teacher.t_file
            user_info.save()
            return HttpResponse('<script type="text/javascript"> alert("회원 정보가 저장되었습니다."); location.href = "/admin";</script>')


    context = {'user' : user}
    return render(request, 'admin/profile.html', context)


# 선생님 사진 설정
def profile_picture(request, t_no):
    user = teacher_tbl.objects.get(t_no = t_no)


    context = {'user' : user}
    if request.method == 'POST':
        # 사진 경로를 teacher_tbl에 저장
        try:
            user.t_file = request.FILES['t_img']
        except:
            return HttpResponse('<script type="text/javascript"> alert("사진을 등록 후 확인을 눌러 주세요,"); history.back();</script>' )
        user.save()

        # 사진 경로를 User테이블에도 저장
        user_info = User.objects.get(id=request.user.id)
        user_info.first_name = user.t_file
        user_info.save()

    return render(request, 'admin/profile_picture.html', context)

# 메인 화면
@user_passes_test(lambda u: u.is_superuser, login_url='admin:login_admin')
def index(request):
    # 전체 선생님 리스트
    teacher_list = teacher_tbl.objects.order_by('t_join')

    # 수학 선생님 리스트
    teacher_math_list = teacher_tbl.objects.filter(t_subject='수학')

    # 영어 선생님 리스트
    teacher_eng_list = teacher_tbl.objects.filter(t_subject='영어')

    # 오늘 날짜
    day = timezone.now()
    context = {'day' : day, 'teacher_list' : teacher_list, 'teacher_math_list' : teacher_math_list, 'teacher_eng_list' : teacher_eng_list}

    return render(request, 'admin/main.html', context)

# 사용자페이지 이미지
# @login_required(lambda u: u.is_superuser, login_url='admin:login_admin')
@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def userpage(request):
    if request.method == 'POST':
        userpage = userpage_tbl(page_img_main = request.FILES['main_img'], page_img_sub1 = request.FILES['sub_img_1'], page_img_sub2 = request.FILES['sub_img_2'])
        userpage.save()
        return redirect('/admin/')
    return render(request, 'admin/userpage.html')

# 현재 선생님
@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def teacher_in(request):
    # 예외 처리를 해 줍니다.(등록된 선생님이 없을 경우 order_by 부분에서 오류가 나므로)
    try:
        teacher_list = teacher_tbl.objects.order_by('t_subject')
    except:
        teacher_list = []

    context = {'teacher_list': teacher_list}

    return render(request, 'admin/teacher_in.html', context)

# 퇴사 선생님
@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def teacher_out(request):
    if request.method == 'POST':
        print(request.POST)
        teacher_info = teacher_tbl.objects.get(pk=request.POST['t_no'])
        teacher_info.t_state = True
        teacher_info.t_out = None
        teacher_info.save()

    teacher_list = teacher_tbl.objects.order_by
    day = timezone.now()
    context = {'teacher_list': teacher_list, 'day' : day}

    return render(request, 'admin/teacher_out.html', context)

# 선생님 상세
@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def teacher_detail(request, teacher_tbl_t_no):
    """
    선생님 상세
    """
    if request.method == 'POST':
        # 퇴사 버튼을 눌렀을 경우
        if request.POST['버튼'] == '1':
            # 해당 선생님의 객체를 불러옵니다.
            teacher_info = teacher_tbl.objects.get(pk = teacher_tbl_t_no)
            # 재직 여부의 속성을 False
            teacher_info.t_state = False
            # 퇴사일에 현재 시간을 저장합니다.
            teacher_info.t_out = timezone.now()
            teacher_info.save()

            # 해당 창을 닫고(상세 창), 부모창(선생님 리스트)을 다시 현재 선생님 페이지로 이동시킵니다.(최신화 하기 위해)
            return HttpResponse('<script type="text/javascript">window.close(); window.opener.parent.location.href = "../teacher.in";</script>' )

        # 저장 버튼을 눌렀을 경우
        elif request.POST['버튼'] == '2':
            # 해당 선생님의 객체를 불러옵니다.
            teacher_info = teacher_tbl.objects.get(pk=teacher_tbl_t_no)
            # 선생님 특이사항을 저장합니다.
            teacher_info.t_text = request.POST['t_text']
            teacher_info.save()

            lecture_list = lecture_tbl.objects.filter(t_no_id=teacher_info.t_no)

            context = {'teacher_info': teacher_info, 'lecture_list': lecture_list}

            return render(request, 'admin/teacher-detail.html', context)

    teacher_info = teacher_tbl.objects.get(pk=teacher_tbl_t_no)

    # 해당 선생님의 기본키(t_no)를 통해 해당 선생님이 강의하고 있는 강의 리스트를 필터를 통해 가져온다.
    lecture_list = lecture_tbl.objects.filter(t_no_id=teacher_info.t_no)
    context = {'teacher_info': teacher_info, 'lecture_list': lecture_list}

    return render(request, 'admin/teacher-detail.html', context)

# 수강생
@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def student_in(request):
    customer_list = customer_tbl.objects.order_by
    context = {'customer_list' : customer_list}

    return render(request, 'admin/student-in.html', context)

# 퇴원생
@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def student_out(request):
    if request.method == 'POST':
        print(request.POST)
        customer_info = customer_tbl.objects.get(pk=request.POST['c_no'])
        customer_info.c_state = True
        customer_info.c_out = None
        customer_info.save()


    customer_list = customer_tbl.objects.order_by
    context = {'customer_list': customer_list}

    return render(request, 'admin/student-out.html', context)

# 학생 상세
@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def student_detail(request, c_no):
    if request.method == 'POST':
        # print(123123,request.POST['1'])
        # print(123,request.POST['버튼'])
        if request.POST['버튼'] == '1':
            # print(123123,teacher_tbl_t_no)
            customer_info = customer_tbl.objects.get(pk = c_no)
            customer_info.c_state = False
            customer_info.c_out = timezone.now()
            customer_info.save()

            lecture_list = lecture_tbl.objects.order_by

            context = {'customer_info' : customer_info, 'lecture_list' : lecture_list}
            return HttpResponse('<script type="text/javascript">window.close(); window.opener.parent.location.href = "../student.in";</script>' )

    try:
        student_info = customer_tbl.objects.get(pk=c_no)
        training_list = training_tbl.objects.filter(c_no_id=c_no)
    except:
        pass
    # 해당 학생이 듣는 강의 객체를 불러옵니다.


    context = {'customer_info': student_info, 'training_list': training_list}

    # student_info = customer_tbl.objects.get(pk=c_no)
    # context = {'customer_info': student_info}

    return render(request, 'admin/student-detail.html', context)

# 강의 등록
@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def lecture_create(request):
    """
    lecture 등록
    """
    if request.method == 'POST':
        form_teacher = LectureForm_teacher(request.POST)
        form = LectureForm()

        # 1번 버튼을 눌렀을 때(선생님 선택)
        if request.POST['버튼'] == '1':
            print(request.POST)
            teacher_info = teacher_tbl.objects.get(pk=request.POST['t_no'])
            # form_teacher = LectureForm_teacher(request.POST)
            teacher_t_no = request.POST['t_no']

            context = { 'teacher_info' : teacher_info, 'form_teacher' : form_teacher, 'form' :form, 'teacher_t_no' : teacher_t_no }

            return render(request, 'admin/lecture_form.html', context)

        # 2번 버튼을 눌렀을 때(등록하기)
        if request.POST['버튼'] == '2':

            try:
                form = LectureForm(request.POST)
                print(request.POST)
                lecture_tbl = form.save(commit=False)
                lecture_tbl.t_no_id = request.POST['gg']
                lecture_tbl.l_img = request.FILES['l_img']
                lecture_tbl.save()
                return redirect('admin:index')
            except:
                messages.error(request, '선생님을 선택하신 후 선택 버튼을 눌러주세요')


    else:
        form = LectureForm()
        # form_teacher = LectureForm_teacher()

    teacher_list = teacher_tbl.objects.order_by
    context = {'form' : form, 'teacher_list' : teacher_list}

    return render(request, 'admin/lecture_form.html', context)

# 학부모 목록
@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def parents_list(request):
    customer_list = customer_tbl.objects.order_by
    # customer_tbl.objects.get(pk = )

    context = {'customer_list': customer_list}


    return render(request, 'admin/parent_list.html', context)

# 로그인
def login_admin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # authenticate 함수를 사용하여 인증과정을 거칩니다. 인증이 되지 않으면 None을 리턴합니다.
        user = authenticate(username = username, password=password)
        if user is not None:
            login(request, user)

            return redirect('/admin')
        # 정보가 틀렸을 시 새로운 스크립트에 메세지를 띄우고 확인 시 원래창으로 돌아오기
        else:
            return HttpResponse('<script type="text/javascript"> alert("입력하신 정보가 틀렸습니다. 다시 입력해 주세요."); history.back();</script>' )

    return render(request, 'admin/login.html')

def logout_admin(request):
    logout(request)

    return redirect('/admin')

@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def consult_list(request):
    try:
        consult_list = consult_tbl.objects.order_by('cu_no')
    except:
        pass

    context = {'consult_list': consult_list}
    return render(request, 'admin/consult_list.html', context)



@user_passes_test(lambda u: u.is_superuser, login_url='admin:login_admin')
# 학생,학부모 가입자수 통계 데이터 넘기기
def chart_customer_data(request):
    try:
        customer_list = customer_tbl.objects.order_by('c_join')
    except:
        customer_list = []

    date = ['날짜', ]
    count = ['가입자 수', ]

    for customer in customer_list:
        # 가입일을 str 형태로 변환
        c_join = customer.c_join.strftime('%Y-%m-%d')
        # 리스트에 추가
        if c_join in date:
            # c_join 이 date리스트에 이미 있다면 count의 마지막 인덱스의 값을 1올림
            count[-1] += 1
        # 그렇지 않을 경우(c_join이 date에 없을 경우)
        else:
            # c_join을 date리스트에 추가
            date.append(c_join)
            # count리스트에 1 추가
            count.append(1)

    # x축(날짜)와 y축(매출액) 변수로 넘기기
    data = {
        'columns': [
            date,
            count,
        ]
    }
    return HttpResponse(json.dumps(data), content_type='text/json')


@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
# (선생님)가입자 수 통계 데이터 넘기기
def chart_data(request):

    # 선생님 통계
    try:
        teacher_list = teacher_tbl.objects.order_by('t_join')
    except:
        pass

    # print(training_list)
    date = ['날짜',]
    count = ['가입자 수',]

    for teacher in teacher_list:
        # 가입일을 str 형태로 변환
        t_join = teacher.t_join.strftime('%Y-%m-%d')
        # 리스트에 추가
        if t_join in date:
            # t_join 이 date리스트에 이미 있다면 count의 마지막 인덱스의 값을 1올림
            count[-1] += 1
        # 그렇지 않을 경우(t_join이 date에 없을 경우)
        else:
            # t_join을 date리스트에 추가
            date.append(t_join)
            # count리스트에 1 추가
            count.append(1)

    print(date)
    print(count)


    # x축(날짜)와 y축(매출액) 변수로 넘기기
    data = {

        'columns': [
            date,

            count,
        ]
    }

    return HttpResponse(json.dumps(data), content_type='text/json')

# 병훈 --------------------------------------------------------------

# #공지 등록하기
# @user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
# def notice(request):
#     """
#     notice 등록
#     """
#     if request.method == 'POST':
#         form = NoticeForm(request.POST)
#         if form.is_valid():
#             notice_tbl = form.save(commit=False)
#             notice_tbl.n_writer = "관리자"
#             notice_tbl.notice_date = timezone.now()
#             notice_tbl.save()
#
#             return redirect('admin:index')
#     else:
#         form = NoticeForm()
#     context = {'form': form}
#     return render(request, 'admin/notice.html', context)
#
#
# #공지 목록 보기
# @user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
# def noticelist(request):
#     if notice_tbl.objects.order_by('notice_no'):
#         notice_list = notice_tbl.objects.order_by('notice_no')
#         print(notice_list)
#     context = {'notice_list':notice_list}
#     return render(request,'admin/noticelist.html',context)
#
# #자주하는 질문 등록하기
# @user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
# def faq(request):
#     """
#     Faq 등록
#     """
#     if request.method == 'POST':
#         form = FaqForm(request.POST)
#         if form.is_valid():
#             faq_tbl = form.save(commit=False)
#             faq_tbl.faq_date = timezone.now()
#             faq_tbl.save()
#
#             return redirect('admin:index')
#     else:
#         form = FaqForm()
#     context = {'form': form}
#     return render(request,'admin/faq.html',context)
#
#
# #자주하는 질문 리스트
#
# @user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
# def faqlist(request):
#     if faq_tbl.objects.order_by('faq_no'):
#         faq_list = faq_tbl.objects.order_by('faq_no')
#     # faq_list_detail = []
#     context = {'faq_list': faq_list}
#     return render(request, 'admin/faqlist.html', context)
#
# #공지상세
# @user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
# def noticedetail(request, notice_tbl_t_no):
#     """
#     detail 내용 출력 삭제 수정
#     """
#     if request.method =='POST':
#         if request.POST['버튼'] == '1':
#
#            noticeinfo = notice_tbl.objects.get(pk=notice_tbl_t_no)
#            noticeinfo.delete()
#
#            # context = {'noticeinfo':noticeinfo}
#            return redirect('../noticelist')
#     if request.method == 'POST':
#         if request.POST['버튼'] == '2':
#
#             # print([title])
#             noticeinfo = notice_tbl.objects.get(pk=notice_tbl_t_no)
#
#             noticeinfo.notice_title = request.POST['title']
#             noticeinfo.notice_content =request.POST['content']
#             noticeinfo.notice_date = timezone.now()
#             noticeinfo.save()
#
#             # ttt = {'noticeinfo': noticeinfo}
#             return redirect('../noticelist')
#
#     detail = notice_tbl.objects.get(pk = notice_tbl_t_no)
#     context = {'detail':detail}
#     return render(request,'admin/noticedetail.html',context)
#
# @user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
# def faqdetail(request,faq_tbl_t_no):
#     """
#     faq 내용 출력 삭제 수정
#     """
#     if request.method == 'POST':
#         if request.POST['버튼'] == '1':
#             faqinfo = faq_tbl.objects.get(pk=faq_tbl_t_no)
#             faqinfo.delete()
#
#             # context = {'noticeinfo':noticeinfo}
#             return redirect('../faqlist')
#     if request.method == 'POST':
#         if request.POST['버튼'] == '2':
#             # print([title])
#             faqinfo = faq_tbl.objects.get(pk=faq_tbl_t_no)
#
#             faqinfo.faq_question = request.POST['title']
#             faqinfo.faq_answer = request.POST['content']
#             faqinfo.faq_date = timezone.now()
#             faqinfo.save()
#
#             # ttt = {'noticeinfo': noticeinfo}
#             return redirect('../faqlist')
#
#     detail = faq_tbl.objects.get(pk=faq_tbl_t_no)
#     context = {'detail': detail}
#
#
#     return render(request,'admin/faqdetail.html',context)
#
#
#
# def payment(request):
#     # t = teacher_tbl.objects.order_by
#     # c = customer_tbl.objects.order_by
#     # l = lecture_tbl.objects.order_by
#     tr = training_tbl.objects.order_by
#     # payment_list = t,c
#     # payment_list = customer_tbl.c_name, customer_tbl.c_id, lecture_tbl.l_dept, lecture_tbl.l_subject,\
#     #                teacher_tbl.t_name, training_tbl.tr_date, lecture_tbl.l_pay
#
#     context = {'tr':tr}
#
#
#     return render(request,'admin/payment.html', context)


#공지 등록하기
def notice(request):
    """
    notice 등록
    """
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice_tbl = form.save(commit=False)
            notice_tbl.notice_date = timezone.now()
            notice_tbl.save()

            return redirect('admin:noticelist')
    else:
        form = NoticeForm()
    context = {'form': form}
    return render(request, 'admin/notice.html', context)


#공지 목록 보기
def noticelist(request):
    notice_list = notice_tbl.objects.order_by
    context = {'notice_list':notice_list}
    return render(request,'admin/noticelist.html',context)

#공지상세
def noticedetail(request, notice_tbl_t_no):
    """
    detail 내용 출력 삭제
    """
    if request.method =='POST':
        if request.POST['버튼'] == '1':

           noticeinfo = notice_tbl.objects.get(pk=notice_tbl_t_no)
           noticeinfo.delete()

           # context = {'noticeinfo':noticeinfo}
           return redirect('../noticelist')
    if request.method == 'POST':
        if request.POST['버튼'] == '2':

            # print([title])
            noticeinfo = notice_tbl.objects.get(pk=notice_tbl_t_no)

            # noticeinfo.notice_title = request.POST['title']
            # noticeinfo.notice_content =request.POST['content']
            # noticeinfo.notice_date = timezone.now()
            # noticeinfo.save()
            # ttt = {'noticeinfo': noticeinfo}
            # context = {'noticeinfo':noticeinfo}
            # return redirect('../noticemodify',context)

    detail = notice_tbl.objects.get(pk = notice_tbl_t_no)
    context = {'detail':detail}
    return render(request,'admin/noticedetail.html',context)

def noticemodify(request,notice_tbl_t_no):

    noticeinfo = notice_tbl.objects.get(pk=notice_tbl_t_no)
    if request.method == 'POST':
        if request.POST['버튼'] == '2':

            # print([title])
            noticeinfo = notice_tbl.objects.get(pk=notice_tbl_t_no)

            noticeinfo.notice_title = request.POST['title']
            noticeinfo.notice_content = request.POST['content']
            noticeinfo.notice_date = timezone.now()
            noticeinfo.save()
            context = {'noticeinfo':noticeinfo}

            return redirect('/admin/noticelist',context)
    detail = notice_tbl.objects.get(pk=notice_tbl_t_no)
    context = {'detail':detail}
    return render(request, 'admin/noticemodify.html', context)

#자주하는 질문 등록하기
def faq(request):
    """
    Faq 등록
    """
    if request.method == 'POST':
        form = FaqForm(request.POST)
        if form.is_valid():
            faq_tbl = form.save(commit=False)
            faq_tbl.faq_date = timezone.now()
            faq_tbl.save()

            return redirect('admin:index')
    else:
        form = FaqForm()
    context = {'form': form}
    return render(request,'admin/faq.html',context)

#자주하는 질문 리스트
def faqlist(request):
    faq_list = faq_tbl.objects.order_by
    context = {'faq_list': faq_list}
    return render(request, 'admin/faqlist.html', context)

def faqdetail(request,faq_tbl_t_no):
    """
    faq 내용 출력 삭제 수정
    """
    if request.method == 'POST':
        if request.POST['버튼'] == '1':
            faqinfo = faq_tbl.objects.get(pk=faq_tbl_t_no)
            faqinfo.delete()

            # context = {'noticeinfo':noticeinfo}
            return redirect('../faqlist')
    if request.method == 'POST':
        if request.POST['버튼'] == '2':
            # print([title])
            faqinfo = faq_tbl.objects.get(pk=faq_tbl_t_no)

            faqinfo.faq_question = request.POST['title']
            faqinfo.faq_answer = request.POST['content']
            faqinfo.faq_date = timezone.now()
            faqinfo.save()

            # ttt = {'noticeinfo': noticeinfo}
            return redirect('../faqlist')

    detail = faq_tbl.objects.get(pk=faq_tbl_t_no)
    context = {'detail': detail}


    return render(request,'admin/faqdetail.html',context)

#자주하는 질문 수정
def faqmodify(request,faq_tbl_t_no):
    if request.method == 'POST':
        if request.POST['버튼'] == '2':
            # print([title])
            faqinfo = faq_tbl.objects.get(pk=faq_tbl_t_no)

            faqinfo.faq_question = request.POST['title']
            faqinfo.faq_answer = request.POST['content']
            faqinfo.faq_date = timezone.now()
            faqinfo.save()

            # ttt = {'noticeinfo': noticeinfo}
            return redirect('../faqlist')

    detail = faq_tbl.objects.get(pk=faq_tbl_t_no)
    context = {'detail': detail}


    return render(request,'admin/faqmodify.html',context)






def payment(request):
    # t = teacher_tbl.objects.order_by
    # c = customer_tbl.objects.order_by
    # l = lecture_tbl.objects.order_by
    tr = training_tbl.objects.order_by
    # payment_list = t,c
    # payment_list = customer_tbl.c_name, customer_tbl.c_id, lecture_tbl.l_dept, lecture_tbl.l_subject,\
    #                teacher_tbl.t_name, training_tbl.tr_date, lecture_tbl.l_pay

    context = {'tr':tr}


    return render(request,'admin/payment.html', context)


def lecturelist(requset):
    lecturelist = lecture_tbl.objects.order_by
    teacherlist = teacher_tbl.objects.order_by
    traininglist = training_tbl.objects.order_by
    context = {'lecturelist':lecturelist, 'teacherlist':teacherlist, 'traininglist':traininglist}
    return render(requset, 'admin/lecturelist.html', context)

def lecturemodify(request,lecture_tbl_l_no):



    lecture = lecture_tbl.objects.get(pk=lecture_tbl_l_no)
    # teacher_info = teacher_tbl.objects.get(pk=request.POST['t_no'])
    context = {'lecture': lecture}
    if request.method == 'POST':
        if request.POST['버튼'] == '3':
            print('333')
            lectureinfo = lecture_tbl.objects.get(pk=lecture_tbl_l_no)
            try:
                lectureinfo.delete()
            except:
                return HttpResponse('<script type="text/javascript"> alert("해당 강의를 신청한 학생이 있습니다."); history.back();</script>')

        return redirect('/admin/lecturelist')

    return render(request,'admin/lecturemodify.html',context)

def  lecturemodify2(request,lecture_tbl_l_no):
    lecture = lecture_tbl.objects.get(pk=lecture_tbl_l_no)
    # teacher_info = teacher_tbl.objects.get(pk=request.POST['t_no'])
    context = {'lecture': lecture}
    if request.method == 'POST':

        if request.POST['버튼'] == '2':
            print('333')
            # form = Lecturemodify2Form(request.POST)
            lectureinfo = lecture_tbl.objects.get(pk=lecture_tbl_l_no)
            lectureinfo.l_pay = request.POST['pay']
            lectureinfo.l_totalnum = request.POST['totalnum']
            lectureinfo.l_term = request.POST['term']

            if request.POST['term'] >= '4' or request.POST['term'] == '0':
                return HttpResponse('<script type="text/javascript"> alert("강의 기간은 1개월~3개월 까지 입력 가능합니다."); history.back();</script>')
            lectureinfo.l_desc = request.POST['desc']
            lectureinfo.l_dept = request.POST['dept']
            # if request.POST['dept'] == '중등' and request.POST['dept'] =='고등':
            #     return HttpResponse('<script type="text/javascript"> alert("부서는 중등, 고등으로 입력해 주세요."); history.back();</script>')
            lectureinfo.l_class = request.POST['class']
            if request.POST['class'] >= '4' or request.POST['class'] =='0':
                return HttpResponse('<script type="text/javascript"> alert("학년은 1학년~3학년 까지 입력 가능합니다."); history.back();</script>')
            lectureinfo.l_img = request.FILES['img']
            lectureinfo.l_startdate = request.POST['date']
            lectureinfo.save()


            return redirect('/admin/lecturelist')
        # if request.POST['버튼'] =='2':
        #     form = Lecturemodify2Form(request.POST)
        #     lecture_tbl = form.save(commit=False)
        #     lecture_tbl.l_img = request.FILES['l_img']
        #     lecture_tbl.save()
        #     return render(request,'/admin/lecturelist.html')



    return render(request, 'admin/lecturemodify2.html', context)



