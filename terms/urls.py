from django.urls import path
from .views import *

app_name='terms'

urlpatterns = [
    path('terms/',popup_terms),
    path('policy/',popup_policy),
]