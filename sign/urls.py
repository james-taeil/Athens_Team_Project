from django.conf.urls import url
from django.urls import path

from . import views


urlpatterns = [
    path('', views.sign),
    path('S_TOS',views.s_tos.as_view()),
    path('P_TOS',views.p_tos.as_view()),
    path('T_TOS',views.t_tos.as_view()),
    path('activate_complete',views.activate_complete),

]