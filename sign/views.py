
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View


def sign(request):
    return render(request, 'sign/select_type.html')


class s_tos(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'sign/S_TOS.html')

    def post(self, request, *args, **kwarg):
        if request.POST.get('name1', False) and request.POST.get('name2', False):
            request.session['agreement'] = True
            return redirect('/sign_up/student/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'sign/S_TOS.html')

class p_tos(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'sign/P_TOS.html')

    def post(self, request, *args, **kwarg):
        if request.POST.get('name1', False) and request.POST.get('name2', False):
            request.session['agreement'] = True
            return redirect('/sign_up/parent/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'sign/P_TOS.html')

class t_tos(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'sign/T_TOS.html')

    def post(self, request, *args, **kwarg):
        if request.POST.get('name1', False) and request.POST.get('name2', False):
            request.session['agreement'] = True
            return redirect('/sign_up/teacher/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'sign/T_TOS.html')

def activate_complete(request):
    return render(request, 'sign/activate_complete.html')