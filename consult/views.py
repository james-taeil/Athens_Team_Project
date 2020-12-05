from django.contrib.auth.decorators import *
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from admin.models import *
from .forms import reservationform, timeform
from django.utils import timezone

# Create your views here.

# 예약
@login_required(login_url='/login/login')
# @permission_required('admin.can_view_consult',login_url='/main')
def reservation(request):
    id = request.user.id
    parent = customer_tbl.objects.get(user_id=id)
    children = customer_tbl.objects.filter(c_code=parent.c_code_valid)
    form = timeform()
    timeset = ''
    set_timeset = False
    set_teacher = False
    error = False
    lecture_list=[]
    context = {'set_timeset':set_timeset,'set_teacher':set_teacher,'children': children}
    if request.method == 'POST':
        if request.POST['button'] == 'c':
            child = request.POST['children']
            default_child = customer_tbl.objects.get(c_no=child)
            training = training_tbl.objects.filter(c_no_id=child)
            for i in range(len(training)):
                lecture = training[i].l_no
                lecture_list.append(lecture)
            set_teacher = True
            context={'set_teacher':set_teacher,'lecture_list':lecture_list,'default_child':default_child,'children': children,'error':error}
            return render(request, 'consult/reservation.html', context)
        if request.POST['button'] == 'l':
            try:
                child = customer_tbl.objects.get(c_no=request.POST['children'])
                lecture = lecture_tbl.objects.get(l_no=request.POST['lecture'])
                training_tbl.objects.get(c_no_id=child.c_no,l_no_id=lecture.l_no)
                set_timeset=True
                context = {'set_teacher': set_teacher, 'lecture': lecture,'default_child':child,'children': children,'set_timeset':set_timeset}
            except:
                error=True
                context = {'set_teacher': set_teacher, 'lecture_list': lecture_list, 'children': children,'error': error}
                return render(request,'consult/reservation.html',context)
        if request.POST['button'] == '1':
            child = customer_tbl.objects.get(c_no=request.POST['children'])
            lecture = lecture_tbl.objects.get(l_no=request.POST['lecture'])
            form=timeform()
            timeset = 1
            set_timeset = True
            context = {'set_teacher': set_teacher, 'lecture': lecture, 'default_child':child,'children': children, 'set_timeset': set_timeset, 'timeset': timeset,'time_form':form}
            return render(request, 'consult/reservation.html', context)
        if request.POST['button'] == '2':
            child = customer_tbl.objects.get(c_no=request.POST['children'])
            lecture = lecture_tbl.objects.get(l_no=request.POST['lecture'])
            form=timeform()
            timeset = 2
            set_timeset = True
            context = {'set_teacher': set_teacher, 'lecture': lecture, 'default_child':child, 'children': children, 'set_timeset': set_timeset, 'timeset': timeset,'time_form':form}
            return render(request, 'consult/reservation.html', context)
        if request.POST['button'] == '3':
            lecture = lecture_tbl.objects.get(l_no=request.POST['lecture'])
            set_lecture = lecture_tbl.objects.get(l_no=request.POST['lecture'])
            teacher = teacher_tbl.objects.get(t_no=set_lecture.t_no_id)
            try:
                consult_tbl.objects.get(t_no_id=teacher.t_no,cu_res_time=request.POST['cu_res_time'])
                time_error=True
                context = {'set_teacher': set_teacher, 'lecture': lecture, 'children': children,
                           'set_timeset': set_timeset, 'timeset': timeset, 'time_form': form, 'time_error':time_error}
                return render(request, 'consult/reservation.html', context)
            except:
                parent=customer_tbl.objects.get(user_id=request.user)
                child=customer_tbl.objects.get(c_no=request.POST['children'])
                consult_tbl.objects.create(cu_res_time=request.POST['cu_res_time'],cu_join_time=timezone.now(),cu_state='상담대기',cu_text=request.POST['cu_text'],c_no_id=parent.c_no,t_no_id=teacher.t_no,cu_student=child.c_name)
                return redirect('/')
    return render(request,'consult/reservation.html',context)



# 상담 관리
@user_passes_test(lambda u: u.is_staff,login_url='/login')
def reservation_manage(request):
    teacher = teacher_tbl.objects.get(user=request.user.id)
    schedule = consult_tbl.objects.filter(t_no_id=teacher.t_no).exclude(cu_state='취소').order_by('cu_res_time')
    # 페이징
    page = request.GET.get('page', '1')  # 페이지
    paginator = Paginator(schedule, 5)  # 페이지당 5개
    page_obj = paginator.get_page(page)
    context = {'schedule': page_obj}
    if request.method == "POST":

        if request.POST['button'] == "1":
            return redirect('/consult/teacher/manage/')

        if request.POST['button'] == "2":
            schedule = consult_tbl.objects.filter(t_no_id=teacher.t_no,cu_state='상담대기').order_by('cu_res_time')
            # 페이징
            page = request.GET.get('page', '1')  # 페이지
            paginator = Paginator(schedule, 5)  # 페이지당 5개
            page_obj = paginator.get_page(page)
            context = {'schedule': page_obj}
            return render(request, 'consult/reservation_manage.html', context)

        if request.POST['button'] == "3":
            schedule = consult_tbl.objects.filter(t_no_id=teacher.t_no,cu_state='상담완료').order_by('cu_res_time')
            # 페이징
            page = request.GET.get('page', '1')  # 페이지
            paginator = Paginator(schedule, 5)  # 페이지당 5개
            page_obj = paginator.get_page(page)
            context = {'schedule': page_obj}
            return render(request, 'consult/reservation_manage.html', context)

    return render(request,'consult/reservation_manage.html',context)

@user_passes_test(lambda u: u.is_staff,login_url='/login')
def reservation_content(request,pk):

    content = consult_tbl.objects.get(pk=pk)
    if request.method == "POST":
        return redirect('/consult/teacher/update/%s' %(pk))

    context = {'content':content}
    return render(request,'consult/reservation_content.html',context)

@user_passes_test(lambda u: u.is_staff,login_url='/login')
def consult_update(request,pk):

    content = consult_tbl.objects.get(pk=pk)
    context = {'content':content}
    if request.method == "POST":
        content.cu_content= request.POST['cu_content']
        content.cu_state='상담완료'
        content.save()
        return redirect('/consult/teacher/manage/%s' %(pk))
    else:
        return render(request, 'consult/consult_update.html', context)

#사용자 페이지 상담예약
@login_required(login_url='/login/login')
# @permission_required('admin.can_view_consult',login_url='/main')
def mainreservation(request):
    id = request.user.id
    parent = customer_tbl.objects.get(user_id=id)
    children = customer_tbl.objects.filter(c_code=parent.c_code_valid)
    form = timeform()
    timeset = ''
    set_timeset = False
    set_teacher = False
    error = False
    lecture_list=[]
    context = {'set_timeset':set_timeset,'set_teacher':set_teacher,'children': children}
    if request.method == 'POST':
        if request.POST['button'] == 'c':
            child = request.POST['children']
            default_child = customer_tbl.objects.get(c_no=child)
            try:
                training = training_tbl.objects.filter(c_no_id=child)
                for i in range(len(training)):
                    lecture = training[i].l_no
                    lecture_list.append(lecture)
                set_teacher = True
                if lecture_list == []:
                    set_teacher = False
            except:
                pass
            context={'set_teacher':set_teacher,'lecture_list':lecture_list,'default_child':default_child,'children': children,'error':error}
            return render(request, 'consult/mainpage_reservation.html', context)
        if request.POST['button'] == 'l':
            try:
                child = customer_tbl.objects.get(c_no=request.POST['children'])
                lecture = lecture_tbl.objects.get(l_no=request.POST['lecture'])
                training_tbl.objects.get(c_no_id=child.c_no,l_no_id=lecture.l_no)
                set_timeset=True
                context = {'set_teacher': set_teacher, 'lecture': lecture,'default_child':child,'children': children,'set_timeset':set_timeset}
            except:
                error=True
                context = {'set_teacher': set_teacher, 'lecture_list': lecture_list, 'children': children,'error': error}
                return render(request,'consult/mainpage_reservation.html',context)
        if request.POST['button'] == '1':
            child = customer_tbl.objects.get(c_no=request.POST['children'])
            lecture = lecture_tbl.objects.get(l_no=request.POST['lecture'])
            form=timeform()
            timeset = 1
            set_timeset = True
            context = {'set_teacher': set_teacher, 'lecture': lecture, 'default_child':child,'children': children, 'set_timeset': set_timeset, 'timeset': timeset,'time_form':form}
            return render(request, 'consult/mainpage_reservation.html', context)
        if request.POST['button'] == '2':
            child = customer_tbl.objects.get(c_no=request.POST['children'])
            lecture = lecture_tbl.objects.get(l_no=request.POST['lecture'])
            form=timeform()
            timeset = 2
            set_timeset = True
            context = {'set_teacher': set_teacher, 'lecture': lecture, 'default_child':child, 'children': children, 'set_timeset': set_timeset, 'timeset': timeset,'time_form':form}
            return render(request, 'consult/mainpage_reservation.html', context)
        if request.POST['button'] == '3':
            lecture = lecture_tbl.objects.get(l_no=request.POST['lecture'])
            set_lecture = lecture_tbl.objects.get(l_no=request.POST['lecture'])
            teacher = teacher_tbl.objects.get(t_no=set_lecture.t_no_id)
            try:
                consult_tbl.objects.get(t_no_id=teacher.t_no,cu_res_time=request.POST['cu_res_time'])
                time_error=True
                context = {'set_teacher': set_teacher, 'lecture': lecture, 'children': children,
                           'set_timeset': set_timeset, 'timeset': timeset, 'time_form': form, 'time_error':time_error}
                return render(request, 'consult/mainpage_reservation.html', context)
            except:
                parent=customer_tbl.objects.get(user_id=request.user)
                child=customer_tbl.objects.get(c_no=request.POST['children'])
                consult_tbl.objects.create(cu_res_time=request.POST['cu_res_time'],cu_join_time=timezone.now(),cu_state='상담대기',cu_text=request.POST['cu_text'],c_no_id=parent.c_no,t_no_id=teacher.t_no,cu_student=child.c_name)
                return redirect('/main')
    return render(request,'consult/mainpage_reservation.html',context)


#상담취소
@login_required(login_url='/login/login')
def reservation_cancel(request):
    id = request.user.id
    par_id = customer_tbl.objects.get(user_id=id)
    consult_info = consult_tbl.objects.filter(c_no_id=par_id)
    context = {'consult_info': consult_info}
    count = 0
    if request.method == "POST":
        cuno = request.POST['btn']
        cu_st = consult_tbl.objects.get(cu_no=cuno)
        cu_st.cu_state = '상담취소'
        cu_st.cu_res_time = None
        cu_st.save()
    for i in consult_info:
        if i.cu_state == "상담대기":
            count += 1
    context = {'consult_info': consult_info, 'count':count}
    return render(request, 'consult/reservation_cancel.html', context)