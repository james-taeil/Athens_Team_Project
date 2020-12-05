from django.urls import path
# from . import views
from django.conf.urls import url
import chart.views

app_name = 'chart'

urlpatterns = [
    # path('', main_page.index, name='chart'),
    # path('api/result/', views.ResultAPIView.as_view(), name="result_api"),
    # path('result/', views.result_detail, name='result_detail'),
    url(r'^test$', chart.views.test_page),
    url(r'^chart.data$', chart.views.chart_data, name = 'chart_data'),
    url(r'^chart.data2$', chart.views.chart_data2, name = 'chart_data2'),
    url(r'^chart$', chart.views.main_page, name = 'sales_chart'),
    url(r'^teacher$', chart.views.teacher, name = 'teacher_chart'),
    url(r'^chart.teacher$', chart.views.chart_teacher, name = 'chart_teacher'),
]