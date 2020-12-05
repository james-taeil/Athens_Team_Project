
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import *
from .helper import email_auth_num, send_mail




def C_find(request):
    if request.method == 'POST':
        form = C_ID_find(request.POST)
        if form.is_valid():
            c_name = request.POST['c_name']
            c_phone = request.POST['c_phone']
            try:
                # 일치할 때
                c_info = customer_tbl.objects.get(c_name=c_name, c_phone=c_phone)
                return HttpResponse(
                    '<script type="text/javascript">alert("입력된 정보로 가입된 계정은' + c_info.user.username + '입니다."); location.href  ="/login/login"; </script>')
            except:
                # 일치 하는게 없을 때
                return HttpResponse('<script type="text/javascript">alert("가입된 계정이 없습니다."); history.back(); </script>')

    form = C_ID_find()
    context = {'form': form}
    return render(request, 'find/ID_find.html', context)


def T_find(request):
    if request.method == 'POST':
        form = T_ID_find(request.POST)
        if form.is_valid():
            t_name = request.POST['t_name']
            t_phone = request.POST['t_phone']
            try:
                # 일치할 때
                t_info = teacher_tbl.objects.get(t_name=t_name, t_phone=t_phone)
                return HttpResponse(
                    '<script type="text/javascript">alert("입력된 정보로 가입된 계정은' + t_info.user.username + '입니다."); location.href  = "/login/login" ; </script>')
            except:
                # 일치 하는게 없을 때
                return HttpResponse('<script type="text/javascript">alert("가입된 계정이 없습니다."); history.back(); </script>')

    form = T_ID_find()
    context = {'form': form}
    return render(request, 'find/T_ID_find.html', context)


def pw_find(request):

    if request.method == 'POST':

        form = PW_find(request.POST)
        if request.POST['btn'] == '1':
            if request.POST['username']:
                username = request.POST['username']
                try:
                    # 일치할 때
                    info = User.objects.get(username=username)
                except:
                    return HttpResponse(
                        '<script type="text/javascript">alert("가입된 계정이 없습니다."); history.back(); </script>')

                # 학생/학부모일 경우
                try:
                    user_info = customer_tbl.objects.get(user_id=info.id)
                    auth_num = email_auth_num()
                    user_info.c_auth = auth_num
                    user_info.save()
                except:
                    pass
                # 선생님일 경우
                try:
                    user_info = teacher_tbl.objects.get(user_id=info.id)
                    auth_num = email_auth_num()
                    user_info.t_auth = auth_num
                    user_info.save()

                except:
                    pass


                send_mail(
                    '비밀번호 찾기 인증메일입니다.',
                    [username],
                    html=render_to_string('find/recovery_email.html', {
                        'auth_num': auth_num,
                    }),
                )

                context = {'info': user_info}
                return render(request, 'find/PW_find.html', context)


        # 버튼 2번을 눌렀을 때
        if request.POST['btn'] == '2':
            input_auth_num = request.POST['input_auth_num']
            try:
                if customer_tbl.objects.get(c_auth=input_auth_num):
                    c_info = customer_tbl.objects.get(c_auth=input_auth_num)
                    user = User.objects.get(pk=c_info.user_id)
                    user.set_password(input_auth_num)
                    user.save()
                    c_info.c_auth = ""
                    c_info.save()
                    return HttpResponse(
                        '<script type="text/javascript">alert("인증성공. 임시비밀번호로 설정되었습니다."); location.href  = "/login/login" ; </script>')

                if teacher_tbl.objects.get(t_auth=input_auth_num):
                    t_info = teacher_tbl.objects.get(t_auth=input_auth_num)
                    user = User.objects.get(pk=t_info.user_id)
                    user.set_password(input_auth_num)
                    User.save()
                    t_info.c_auth = ""
                    t_info.save()

                    return HttpResponse(
                        '<script type="text/javascript">alert("인증성공. 임시비밀번호로 설정되었습니다."); location.href  = "login/login" ; </script>')
            except:
                return HttpResponse(
                    '<script type="text/javascript">alert("인증번호가 틀립니다."); history.back(); </script>')


        return render(request, 'find/PW_find.html')

    form = PW_find()
    context = {'form': form}
    return render(request, 'find/PW_find.html', context)




