#### 2020년 11월 18일 ####

from admin.models import *
from django.utils import timezone
from django.shortcuts import render, redirect
import requests

# Create your views here.

from django.http import HttpResponse

# 수강신청(결제)
def order(request):
    # 정제된 강의 리스트를 담을 빈 리스트
    lecture_list = []

    try:
        # 강의 리스트(정제전) / 강의 시작일 기준으로 내림차순 정렬 - 최신 강의를 가장 앞쪽에 노출
        lecturelist = lecture_tbl.objects.order_by('-l_startdate')
    except:
        pass

    # 강의리스트 정제하기
    for lecture in lecturelist:
        # 현재 날짜보다 강의 시작날짜가 크거나 같은경우만(현재 날짜 지나면 결제 목록에서 제외)
        if lecture.l_startdate >= timezone.now().date():
            # 강의 목록에 담음
            lecture_list.append(lecture)

    # 수학 강의를 넣을 빈 리스트를 만든다.
    lecture_math_list = []
    for lecture in lecture_list:
        if lecture.t_no.t_subject == '수학':
            lecture_math_list.append(lecture)

    # 영어 강의를 넣을 빈 리스트를 만든다.
    lecture_eng_list = []
    for lecture in lecture_list:
        if lecture.t_no.t_subject == '영어':
            lecture_eng_list.append(lecture)

    ## POST로 요청을 받았을 경우
    if request.method == 'POST':
        print(request.POST)
        if request.POST['btn'] == '자녀선택':
            print(request.POST)
            # 자녀 한명 객체를 선택(요청받은 값)
            student_info = customer_tbl.objects.get(c_no=request.POST['student'])
            context = {'lecture_list': lecture_list, 'lecture_math_list': lecture_math_list,
                       'lecture_eng_list': lecture_eng_list, 'student_info' : student_info}
            return render(request, 'order/order.html', context)

        # 자녀선택이 아닐 때 -> 결제하기를 눌렀을 경우
        else:
            print('하하')
            print(request.POST)
            l_no = request.POST['l_no']
            pay = request.POST['pay']
            t_name = request.POST['t_name']
            print(request.POST['c_no'])

            # c_no값을 넘겨준다. # 학생의 c_no
            c_no = request.POST['c_no']
            # 정보를 다시 저장하고 넘김
            context = {'lecture_list': lecture_list, 'l_no' : l_no, 'l_pay' : pay, 't_name' : t_name, 'c_no' : c_no}
            return render(request, 'order/order.html', context)

    # 학생인 경우와 학부모인 경우를 나눈다.
    # 현재 로그인한 사람의 객체를 가져옵니다.
    # 객체 정보를 가져오지 못할 때 오류가 날 수 있으므로 예외처리를 해준다.
    try:
        customer = customer_tbl.objects.get(user_id=request.user.id)
    except:
        print('일치하는 사용자가 없습니다.')
        return HttpResponse('<script type="text/javascript"> alert("일치하는 사용자가 없습니다."); history.back();</script>')

    # if에 걸리면 학생 그렇지 않으면 학부모
    # 학생인 경우
    if customer.c_code:
        context = {'lecture_list': lecture_list, 'lecture_math_list': lecture_math_list,
                   'lecture_eng_list': lecture_eng_list}
        return render(request, 'order/order.html', context)
    #학부모인 경우
    else:
        # 학부모의 코드인증(c_code_valid)번호와 같은 학생 리스트를 filter를 통해 담아온다. -> student_list에 할당
        student_list = customer_tbl.objects.filter(c_code = customer.c_code_valid)
        # print(student_list)
        # 학부모인 경우는 student_list 추가. (html문서에서 이 정보를 통해 로그인 한 회원에 따라 다른 화면을 보여준다.)
        context = {'lecture_list': lecture_list, 'lecture_math_list': lecture_math_list,
                   'lecture_eng_list': lecture_eng_list, 'student_list' : student_list}
        return render(request, 'order/order.html', context)



#####################################################
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from admin.models import *

def order_create(request):
    print(123123123123+'gkg')
    if request.method == 'POST':
        # form = OrderCreateForm(request.POST)
        # if form.is_valid():
        print('하하')
        print(666666666666666, request.POST)
        # 임의로 1로 지정함(수정필요)
        customer = customer_tbl.objects.get(pk=1).c_no

        Order.objects.create(customer_id=customer)

        l_no = request.POST['l_no']
        # 강의 객체를 가져옴
        lecture = lecture_tbl.objects.get(l_no=l_no)
        # 해당 강의의 가격을 가져온다.
        price = lecture.l_pay
        OrderItem.objects.create(order=order, l_no=l_no, price=price)
        lecture_list = lecture_tbl.objects.order_by
        context = {'lecture_list': lecture_list, 'order': order}
        return render(request, 'order/order.html', context)

    else:
        lecture_list = lecture_tbl.objects.order_by
        context = {'lecture_list' : lecture_list }
    return render(request, 'order/order.html', context)

# ajax로 결제 후에 보여줄 결제 완료 화면

def order_complete(request):
    order_id = request.GET.get('order_id')
    # order = Order.objects.get(id=order_id)
    return render(request,'order/created.html',{'order':order})

# 결제를 위한 임포트
from django.views.generic.base import View
from django.http import JsonResponse

class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        print(request.user)
        # 현재 로그인 되어있는 사람의 user객체를 불러와 current_user에 할당

        print(112312312312,request.POST)
        # 학부모인 경우 자녀 정보 가져오기
        if request.POST['c_no'] != '0':
            print(11111111,request.POST['c_no'])
            customer = customer_tbl.objects.get(c_no=request.POST['c_no'])
        # 학생인 경우('c_no' 가 0인 경우 - html에서 학생인 경우는 c_no를 0으로 보내게 설정했음)
        else:

            current_user = request.user
            # 관계키를 맺는 고객객체를 불러와 customer에 할당
            customer = customer_tbl.objects.get(user_id = current_user.id)
            # Order객체 생성

        order = Order.objects.create(customer_id=customer.c_no)
        # 정수형으로 바꾸어 l_no에 저장

        ########### post값

        print(123123,request.POST)

        l_no = request.POST['l_no']
        # 강의 객체를 가져옴
        lecture = lecture_tbl.objects.get(l_no=l_no)
        # 해당 강의의 가격을 가져온다.
        price = lecture.l_pay
        # OrderItem 객체 생성
        OrderItem.objects.create(order=order, l_no_id=l_no, price=price)

        data = {
            # 생성된 order.id 를 "order_id"라는 변수로 보낸다.
            "order_id": order.id
        }
        return JsonResponse(data)
        # else:
        #     return JsonResponse({}, status=401)

# 결제 정보 생성
class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        # 로그인이 되어있지 않았을 경우
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)
        print(555, request.POST)
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        # 해당하는 orderitem의 객체를 가져온다
        orderitem = OrderItem.objects.get(order_id=order.id)
        # orderitem과 관계를 맺은 강의의 강의료를 가져온다.
        print(orderitem.l_no.l_pay)

        amount = request.POST.get('amount')

        try:
            print('ㅎㅎㅎ')
            # 모델에 있는 create_new 실행
            merchant_order_id = OrderTransaction.objects.create_new(
                order = order,
                amount = amount
            )
        except:
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {
                "works": True,
                "merchant_id": merchant_order_id}
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

# 실제 결과가 이뤄진 것이 있는지 확인
class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        # 로그인이 되어있지 않다면,
        if not request.user.is_authenticated:
            return JsonResponse({"authenticated":False}, status=403)

        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')


        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
        # 트랜잭션 객체가 잡히지 않는다면 tran에 None 을 할당
            trans = None

        # None이 아닐 시(트랜잭션 객체가 생겼을 시) - 나머지 데이터 저장
        if trans is not None:
            trans.transaction_id = imp_id
            # 트랜잭션의 성공여부를 True로 바꾸어준다/
            print('하하')
            trans.success = True
            trans.save()
####-------------------------------##

            # order 테이블의 지불완료를 표시
            order.paid = True
            order.save()
################ 수강 테이블에 데이터 저장 ########################

            # order_item 객체를 가져옴(수강 id 얻기 위해)
            order_item = OrderItem.objects.get(order_id=order.id)
            # 수강 아이디를 얻어옴
            l_no = order_item.l_no.l_no
            # 수강 객체 생성
            training = training_tbl.objects.create(c_no_id=order.customer_id,l_no_id= l_no)
            # 데이터 베이스에 저장
            training.save()


            # 작업을 완료했다는 것을 보내주기 위함.
            data = {
                "works": True
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

# Create your views here.