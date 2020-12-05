from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from admin.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse


#마이페이지 Default 페이지, 개인정보 수정 페이지
def mypage(request):
    user_no = request.user.id
    customer_info = customer_tbl.objects.get(user_id=user_no)  # 사용자 정보 가져오기
    contexts = {'customer_info': customer_info}
    if request.method == "POST":
        # 로그인 한 유저의 객체를 가져온다.
        user_info = request.user
        #확인
        if request.POST['btn'] == '확인':
            username = user_info.username
            password = request.POST['passwd']  # 입력한 비밀번호
            user = authenticate(username = username, password = password)
            context = {'user_info': user_info, 'customer_info' : customer_info}

            if user is not None:
                #개인정보 수정페이지로...
                return render(request, 'mypage/information_insert.html', context)

            else:
                return HttpResponse(
                    '<script type="text/javascript">alert("비밀번호가 틀립니다."); location.href  ="/my"; </script>')

        #저장
        elif request.POST['btn'] == '저장':
            username = user_info.username
            user = authenticate(username=username)
            customer_info.c_phone = request.POST['userphone']
            context = {'user_info': user_info, 'customer_info': customer_info}

            if (request.POST['userphone'] is not '') and (len(request.POST['userphone']) == 11):
                customer_info.c_add = request.POST['useradd']
                customer_info.save()
                return HttpResponse(
                '<script type="text/javascript">alert("수정되었습니다."); location.href  ="/my"; </script>')
            else:
                return HttpResponse(
                    '<script type="text/javascript">alert("정보를 알맞게 입력해주세요."); history.back(); </script>')
        else:
            return render(request, 'mypage/checkpw.html', contexts)

    return render(request, 'mypage/checkpw.html', contexts)


#비밀번호 변경
def mypagepw(request):
    user_id = request.user.id
    customer_info = customer_tbl.objects.get(user_id=user_id)
    contexts = {'customer_info': customer_info}

    #비밀번호 입력
    if request.method == "POST":
        user = request.user
        input_pw = request.POST.get('passwd')
        #확인버튼 클릭 시
        if request.POST['btn'] == '확인':
            current_name = user.username
            user = authenticate(username = current_name, password = input_pw)
            context = {'user_info' : user, 'customer_info' : customer_info}

            if user is not None:
                #개인정보 수정페이지로...
                return render(request, 'mypage/change_pw.html', context)
            else:
                return HttpResponse(
                    '<script type="text/javascript">alert("비밀번호가 틀립니다."); location.href  ="/my/pw"; </script>')

        elif request.POST['btn'] == "저장":
            origin = request.POST.get('userpw')
            if check_password(origin, user.password):
                new_password = request.POST.get('newuserpw')
                password_confirm = request.POST.get('newuserpwcheck')
                if origin == new_password:
                    return HttpResponse(
                        '<script type="text/javascript">alert("기존비밀번호와 다르게 입력해 주세요."); history.back(); </script>')
                if (len(new_password) < 8) or (len(new_password) > 12):
                    return HttpResponse(
                        '<script type="text/javascript">alert("비밀번호는 최소 8자리, 최대 11자리 입니다.."); history.back(); </script>')
                if new_password == password_confirm:
                    user.set_password(new_password)
                    user.save()
                    logout(request)
                    return HttpResponse(
                        '<script type="text/javascript">alert("수정되었습니다. 다시 로그인 해주세요."); location.href  ="/main"; </script>')

                else:
                    return HttpResponse(
                        '<script type="text/javascript">alert("비밀번호가 일치하지 않습니다."); history.back(); </script>')
            else:
                return HttpResponse(
                    '<script type="text/javascript">alert("현재 비밀번호가 다릅니다. 다시 입력해주세요."); location.href  ="/my/pw"; </script>')

    return render(request, 'mypage/changepw_checkpage.html', contexts)

#자녀정보확인
def mychlid(request):
    user_id = request.user.id
    #부모 정보
    customer_info = customer_tbl.objects.get(user_id=user_id)
    context = {'customer_info' : customer_info}
    #부모 코드
    pcode = customer_info.c_code_valid

    #자녀 코드 -- 부모코드 조인
    ccode = customer_tbl.objects.filter(c_code=pcode) # 4번

    #자녀 다수 일 경우
    childlist = []
    for i in ccode:
        childlist.append(i)
    lecture_list = []
    teacherlist = []

    #자녀 선택
    if request.method == 'POST':
        if request.POST['btn'] == '자녀선택':
            student_info = customer_tbl.objects.get(c_no=request.POST['child'])

        training_info = training_tbl.objects.filter(c_no_id=student_info.c_no)

        #강의 전체 정보
        for i in training_info:
            lec_info = lecture_tbl.objects.get(l_no=i.l_no_id)
            lecture_list.append(lec_info)

        #선생님 정보
        for i in lecture_list:
            teacher_info = teacher_tbl.objects.get(t_no=i.t_no_id)
            teacherlist.append(teacher_info)

        # 재원 중일 경우
        if student_info.c_state == 1:
            context = {'customer_info' : customer_info, 'childlist':childlist, 'lecture_list': lecture_list,
                       'student_info':student_info, 'teacherlist':teacherlist}
            return render(request, "mypage/child.html", context)
        else:
            return HttpResponse(
                '<script type="text/javascript">alert("알맞게 입력해 주세요."); history.back(); </script>')

    context = {'customer_info': customer_info, 'childlist': childlist}
    return render(request, "mypage/child.html", context)

    #재원중이 아닐 경우
#자녀 코드 추가 등록
def myaddcode(request):
    #로그인한 부모 정보
    user_id = request.user.id
    customer_info= customer_tbl.objects.get(user_id=user_id)

    #부모 코드
    pcode = customer_info.c_code_valid
    #첫 번째 자녀 정보
    first_child = customer_tbl.objects.filter(c_code=pcode)
    childlist = []
    for i in first_child:
        childlist.append(i)
    first_child = childlist[0]
    contexts = {'customer_info': customer_info, 'first_child': first_child}

    #입력한 자녀 코드
    if request.method == 'POST':
        second_childcode = request.POST['changeusercode']
        if second_childcode is None:
            return  HttpResponse(
                '<script type="text/javascript">alert("등록 되었습니다. "); history.back(); </script>')
        else:
            second_child = customer_tbl.objects.get(c_code=second_childcode)
            second_child.c_code = first_child.c_code

            second_child.save()
            return HttpResponse(
                            '<script type="text/javascript">alert("등록 되었습니다. "); location.href  ="/my/add"; </script>')
    return render(request, 'mypage/addcode.html', contexts)

#결제 내역
def mypagefee(request):
    # 로그인한 부모 정보
    user_id = request.user.id
    customer_info = customer_tbl.objects.get(user_id=user_id)
    cust_no = customer_info.c_no

    trinfo = training_tbl.objects.filter(c_no_id=cust_no)

    lecture_list = []
    for i in range(len(trinfo)):
        lecno = trinfo[i].l_no_id
        lecture_info = lecture_tbl.objects.get(l_no=lecno)
        lecture_list.append(lecture_info)

    contexts = {'customer_info': customer_info, 'lecture_list':lecture_list}
    return render(request, 'mypage/fee.html', contexts)

#선생님 개인정보 수정
def mypageteacher(request):
    user_no = request.user.id
    teacher_info = teacher_tbl.objects.get(user_id=user_no)  # 사용자 정보 가져오기
    contexts = {'teacher_info': teacher_info}
    if request.method == "POST":
        # 로그인 한 유저의 객체를 가져온다.
        user_info = request.user
        if request.POST['btn'] == '확인':
            username = user_info.username
            password = request.POST['passwd']  # 입력한 비밀번호
            user = authenticate(username=username, password=password)
            context = {'user_info': user_info, 'teacher_info': teacher_info}

            if user is not None:
                # 개인정보 수정페이지로...
                return render(request, 'mypage/teacher_info_insert.html', context)
            else:
                return HttpResponse(
                    '<script type="text/javascript">alert("비밀번호가 틀립니다."); location.href  ="/my"; </script>')

        elif request.POST['btn'] == '저장':
            teacher_info.c_phone = request.POST['userphone']
            context = {'user_info': user_info, 'customer_info': teacher_info}
            if (request.POST['userphone'] != " "):
                teacher_info.c_add = request.POST['useradd']
                teacher_info.save()

            else:
                return render(request, 'mypage/teacher_info_insert.html', contexts)  # 템플릿 파일 경로 지정
        else:
            return render(request, 'mypage/teacher_checkpw.html', contexts)

    return render(request, 'mypage/teacher_checkpw.html', contexts)

#선생님 비밀번호 수정
def mypageteacherpw(request):
    user_id = request.user.id
    customer_info = customer_tbl.objects.get(user_id=user_id)
    contexts = {'customer_info': customer_info}

    # 비밀번호 입력
    if request.method == "POST":
        user = request.user
        input_pw = request.POST.get('passwd')
        # 확인버튼 클릭 시
        if request.POST['btn'] == '확인':
            current_name = user.username
            user = authenticate(username=current_name, password=input_pw)
            context = {'user_info': user, 'customer_info': customer_info}

            if user is not None:
                # 개인정보 수정페이지로...
                return render(request, 'mypage/change_pw.html', context)
            else:
                return HttpResponse(
                    '<script type="text/javascript">alert("비밀번호가 틀립니다."); location.href  ="/my"; </script>')

        elif request.POST['btn'] == "저장":
            origin = request.POST.get('userpw')
            if check_password(origin, user.password):
                new_password = request.POST.get('newuserpw')
                password_confirm = request.POST.get('newuserpwcheck')
                if new_password == password_confirm:
                    user.set_password(new_password)
                    user.save()
                    logout(request)
                    return HttpResponse(
                        '<script type="text/javascript">alert("로그아웃 되었습니다. 다시 로그인 해주세요."); location.href  ="/main"; </script>')

                else:
                    HttpResponse(
                        '<script type="text/javascript">alert("오류입니다."); location.href  ="/my/pw"; </script>')

    return render(request, 'mypage/changepw_checkpage.html', contexts)

def mypageattend(request):
    user_id = request.user.id
    customer_info = customer_tbl.objects.get(user_id=user_id)
    cust_no = customer_info.c_no

    trlist = training_tbl.objects.filter(c_no_id=cust_no)

    lecture_list = []
    for i in range(len(trlist)):
        lecno = trlist[i].l_no_id
        lecture_info = lecture_tbl.objects.get(l_no=lecno)
        lecture_list.append(lecture_info)

    attend = []

    for i in range(len(trlist)):
        training_no = trlist[i].tr_no
        attendlist = attendance_tbl.objects.filter(tr_no_id=training_no)
        attend.append(attendlist)

    contexts = {'customer_info': customer_info, 'attend': attend, 'lecture_list': lecture_list}
    return render(request, 'mypage/attendance.html', contexts)

# Create your views here.
