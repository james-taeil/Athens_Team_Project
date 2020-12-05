from django import forms
from admin.models import *


class C_ID_find(forms.ModelForm):
    class Meta:
        model = customer_tbl

        fields = ['c_name', 'c_phone']

        labels = {'c_name': '이름', 'c_phone': '전화번호'}

        widgets = {
            'c_name': forms.TextInput(attrs={'class': 'form-control', 'row': 5}),
            'c_phone': forms.TextInput(attrs={'class': 'form-control', 'row': 5})
        }




class T_ID_find(forms.ModelForm):
    class Meta:
        model = teacher_tbl

        fields = ['t_name', 't_phone']

        labels = {'t_name': '이름', 't_phone': '전화번호'}

        widgets = {
            't_name': forms.TextInput(attrs={'class': 'form-control', 'row': 5}),
            't_phone': forms.TextInput(attrs={'class': 'form-control', 'row': 5})
        }


class PW_find(forms.ModelForm):
    class Meta:
        model = User

        fields = ['username']

        labels = {'username': '이메일'}

        widgets = {
            'user_name': forms.EmailInput(attrs={'class': 'form-control', 'row': 5,  }),
        }


