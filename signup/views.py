from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
import bcrypt, random, string
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from find.helper import send_mail
from .forms import *
from admin.models import customer_tbl,consult_tbl
from django.utils import timezone

from django.contrib.auth.models import User, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


# 학생 회원가입
from .tokens import account_activation_token


def student_sign_up(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        student_form = student_Form(request.POST)
        if user_form.is_valid():

            Student = student_form.save(commit=False)
            username = request.POST['username']
            password = request.POST['password']

            # c_code 생성

            random_code = ''
            string_code = string.ascii_letters + string.digits

            for i in range(6):
                random_code += random.choice(string_code)

            Student.c_code = random_code
            print(random_code)

            #db에 정보 저장

            account=User.objects.create_user(username=username, password=password)
            customer = customer_tbl.objects.get(user=account.id)
            customer.c_name = request.POST['c_name']
            customer.c_phone = request.POST['c_phone']
            customer.c_gender = request.POST['c_gender']
            customer.c_join = timezone.now()
            customer.c_add = request.POST['c_add']
            customer.c_birth = request.POST['c_birth']
            customer.c_school = request.POST['c_school']
            customer.c_code = Student.c_code
            customer.c_state = True
            customer.save()
            # 인증파트
            account.is_active = False  # 유저 비활성화
            account.save()
            current_site = get_current_site(request)
            message = render_to_string('sign_up/activation_email.html', {
                'user': account,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(account.pk)),
                'token': account_activation_token.make_token(account),
            })
            send_mail(
                '계정 활성화 확인 이메일.',
                [username],
                message,
            )

            return redirect("/sign/activate_complete")

    else:
        student_form = student_Form()
        user_form = UserForm()

    context = {'user_form' : user_form,'student_form': student_form }
    return render(request,'sign_up/c_signup.html', context)



# 학부모 회원가입

def parent_sign_up(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        parents_form = parents_Form(request.POST)
        if user_form.is_valid():
            Parents = parents_form.save(commit=False)
            username = request.POST['username']
            password = request.POST['password']


            # 자녀와 동기화

            code_valid = Parents.c_code_valid
            children = customer_tbl.objects.get(c_code=code_valid)
            children.c_code = code_valid
            children.save()

            # User 생성

            account = User.objects.create_user(username=username, password=password)

            # 학부모 권한 부여

            content_type = ContentType.objects.get_for_model(consult_tbl)
            permission = Permission.objects.get(codename='can_view_consult', content_type=content_type, )
            user = get_user_model().objects.all().last()
            user.user_permissions.add(permission)

            # db에 user 정보 저장

            customer = customer_tbl.objects.get(user=account.id)
            customer.c_name = request.POST['c_name']
            customer.c_phone = request.POST['c_phone']
            customer.c_gender = request.POST['c_gender']
            customer.c_join = timezone.now()
            customer.c_add = request.POST['c_add']
            customer.c_birth = request.POST['c_birth']
            customer.c_code_valid = Parents.c_code_valid
            customer.c_state = True
            customer.save()

            # 인증파트
            account.is_active = False  # 유저 비활성화
            account.save()
            current_site = get_current_site(request)
            message = render_to_string('sign_up/activation_email.html', {
                'user': account,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(account.pk)),
                'token': account_activation_token.make_token(account),
            })
            send_mail(
                '계정 활성화 확인 이메일.',
                [username],
                message,
            )

            return redirect("/sign/activate_complete")
    else:
        user_form = UserForm()
        parents_form = parents_Form()
    context = {'user_form' : user_form,'parents_form': parents_form }
    return render(request,'sign_up/p_signup.html', context)

# 선생님 회원가입

def teacher_sign_up(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        teacher_form = teacher_Form(request.POST,request.FILES)
        if user_form.is_valid():
            Teacher = teacher_form.save(commit=False)

            username = request.POST['username']
            password = request.POST['password']

            # db에 저장

            account = User.objects.create_user(username=username, password=password, first_name=Teacher.t_name[0:1], last_name=Teacher.t_name[1:], is_staff=True)
            teacher = teacher_tbl.objects.get(user=account.id)
            teacher.t_name = request.POST['t_name']
            teacher.t_phone = request.POST['t_phone']
            teacher.t_gender = request.POST['t_gender']
            teacher.t_add = request.POST['t_add']
            teacher.t_birth = request.POST['t_birth']
            # 과목
            teacher.t_subject = request.POST['t_subject']
            teacher.t_file = request.FILES['t_file']
            teacher.save()

            # 인증파트
            account.is_active = False  # 유저 비활성화
            account.save()
            current_site = get_current_site(request)
            message = render_to_string('sign_up/activation_email.html', {
                'user': account,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(account.pk)),
                'token': account_activation_token.make_token(account),
            })
            send_mail(
                '계정 활성화 확인 이메일.',
                [username],
                message,
            )

            return redirect("/sign/activate_complete")
    else:
        user_form = UserForm()
        teacher_form = teacher_Form()
    context = {'user_form': user_form, 'teacher_form': teacher_form}

    return render(request, 'sign_up/t_signup.html', context)



#인증파트
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("/login/login")
    else:
        return render(request, 'login/login.html', {'error' : '계정 활성화 오류'})
    return