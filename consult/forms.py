from django import forms
from admin.models import consult_tbl

class reservationform(forms.ModelForm):
    class Meta:
        model = consult_tbl
        fields = ['cu_text']
        labels = {
            'cu_text': '상담 내용',
        }


class timeform(forms.ModelForm):
    class Meta:
        model = consult_tbl
        fields = ['cu_res_time']
        labels = {
            'cu_res_time': '시간 선택',
        }

