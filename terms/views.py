from django.shortcuts import render

# Create your views here.

def popup_terms(request):
    return render(request,'terms.html')

def popup_policy(request):
    return render(request,'privacy_policy.html')