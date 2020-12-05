from django.shortcuts import render, HttpResponse
from admin.models import *
import random, json
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def test_page(request):
    return HttpResponse('hello')

# 매출 통계 차트(해당 년도) - josn파일로 넒기기
def chart_data(request):
    day = timezone.now()
    # 현재년도 스트링으로 받기
    year_now = day.strftime('%Y')
    year_now = int(year_now)

    # print(year_select)
    training_list = training_tbl.objects.order_by('tr_date')
    # print(training_list)
    date = ['날짜', '1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
    cost = ['강의료',0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for training in training_list:

        t = training.tr_date
        # 데이트 type을 str으로 형변환
        date_str = t.strftime('%Y-%m-%d')

        # 년, 월, 일 할당
        year = date_str[:4]
        month = date_str[5:7]
        day = date_str[8:10]

        # 해당 수강번호와 일치하는 강의 리스트
        lecture_list = lecture_tbl.objects.filter(l_no = training.l_no_id)
        print(year, year_now)

        if int(year) == year_now:
            # 강의료
            for lecture in lecture_list:
                print(lecture.l_pay)
                # 해당월에 강의료를 더합니다.
                cost[int(month)] += lecture.l_pay

    # x축(날짜)와 y축(매출액) 변수로 넘기기
    data = {

        'columns': [
            date,

            cost,
        ]
    }

    return HttpResponse(json.dumps(data), content_type='text/json')

# 매출 통계( 전년도 )
def chart_data2(request):
    day = timezone.now()
    # 현재년도 스트링으로 받기
    year_now = day.strftime('%Y')
    year_now = int(year_now)

    # print(year_select)
    training_list = training_tbl.objects.order_by('tr_date')
    # print(training_list)
    date = ['날짜', '1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
    cost = ['강의료',0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for training in training_list:

        t = training.tr_date
        # 데이트 type을 str으로 형변환
        date_str = t.strftime('%Y-%m-%d')

        # 년, 월, 일 할당
        year = date_str[:4]
        month = date_str[5:7]
        day = date_str[8:10]

        # 해당 수강번호와 일치하는 강의 리스트
        lecture_list = lecture_tbl.objects.filter(l_no = training.l_no_id)
        print(year, year_now)

        if int(year)+1 == year_now:
            # 강의료
            for lecture in lecture_list:
                print(lecture.l_pay)
                # 해당월에 강의료를 더합니다.
                cost[int(month)] += lecture.l_pay

    # x축(날짜)와 y축(매출액) 변수로 넘기기
    data = {

        'columns': [
            date,

            cost,
        ]
    }

    return HttpResponse(json.dumps(data), content_type='text/json')


@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def main_page(request):
    # name = '하이'
    day = timezone.now()
    # 현재년도 스트링으로 받기
    year = day.strftime('%Y')
    # 정수형으로 변환
    year = int(year)
    # 콤보박스로 받을 연도를 받을 빈 리스트
    year_list = []
    for i in range(11):
        year_list.append(year-i)


    context = {'year_list' : year_list}
    #  동적으로 받기 위함
    # context = { 'function' : 'chart.data'}
    return render(request, 'chart/chart.html', context)


@user_passes_test(lambda u: u.is_superuser,login_url='admin:login_admin')
def teacher(request):

    return render(request, 'chart/teacher_chart.html')

# 선생님 별 학생 수 데이터 json형태로 보내기
def chart_teacher(request):
    traning_get = training_tbl.objects.order_by('tr_date')
    # 선생님 리스트
    teacher_list = teacher_tbl.objects.order_by('t_no')

    # 선생님을 담을 리스트
    teacher = ['선생님', ]
    # 선생님별 학생수를 담을 리스트
    count = ['수강생 수', ]

    for t in teacher_list:
        # 선생님 이름 리스트에 저장
        teacher.append(t.t_name)
        print(t.t_no)

        # 하나의 강의마다 학생 수 카운트할 빈 리스트(누적합을 구함)
        semi_count = 0
        try:
            # 해당 선생님이 강의하는 강의 리스트
            lecture_list = lecture_tbl.objects.filter(t_no_id=t.t_no)
            print(lecture_list)

            for lecture in lecture_list:
                # 강의 번호와 맞는 수강테이블(training_tbl) 필터링
                training_list = training_tbl.objects.filter(l_no_id=lecture.l_no)

                # 한 강의마다 듣는 학생 수 카운트 해서 semi_count에 누적합(선생님이 강의하는 강의의 총 학생 수)
                semi_count += training_list.count()
        except:
            pass

        # 선생님별 학생수의 누적합을 리스트에 추가
        count.append(semi_count)

    print(teacher)
    print(count)

    data = {

        'columns': [

            teacher,

            count,

        ]

    }

    return HttpResponse(json.dumps(data), content_type='text/json')

