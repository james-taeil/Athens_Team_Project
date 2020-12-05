from django.urls import path
from .views import *

app_name='consult'

urlpatterns = [
    path('',reservation),
    path('main/', mainreservation),
    path('teacher/manage/',reservation_manage),
    path('teacher/manage/<int:pk>',reservation_content),
    path('teacher/update/<int:pk>',consult_update),
    path('cancel/', reservation_cancel),
]