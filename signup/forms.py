from django import forms
from admin.models import customer_tbl,teacher_tbl
from django.contrib.auth.models import User

# 유저 폼
class UserForm(forms.ModelForm):
    re_password = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'class': 'form-control'}),max_length=100)
    class Meta:
        model = User
        fields = ('username', 'password','re_password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username':'아이디',
            'password':'비밀번호'
        }

    # 유효성 검사
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        # 비밀번호 중복
        if password != re_password:
            self.add_error('re_password','비밀번호가 다릅니다.')

        # 비밀번호 8자 미만
        if len(password) < 8:
            self.add_error('re_password','비밀번호는 8자 이상입니다.')

        # 아이디 중복
        try:
            User.objects.get(username=email)
            self.add_error('username','이미 가입된 이메일입니다.')
        except:
            pass

# 학생
class student_Form(forms.ModelForm):
    class Meta:
        model = customer_tbl
        fields = ('c_name','c_phone','c_gender','c_birth','c_add','c_school')

        widgets = {
            'c_name': forms.TextInput(attrs={'class':'form-control'}),
            'c_phone': forms.TextInput(attrs={'class':'form-control'}),
            'c_gender': forms.Select(attrs={'class':'form-control'}),
            'c_add': forms.TextInput(attrs={'class':'form-control'}),
            'c_school':forms.TextInput(attrs={'class':'form-control'}),
        }

        labels = {
            'c_name' : '이름',
            'c_phone' : '전화번호',
            'c_gender' : '성별',
            'c_birth' : '생년월일',
            'c_add' : '주소',
            'c_school': '학교'
        }

# 학부모
class parents_Form(forms.ModelForm):
    class Meta:
        model = customer_tbl
        fields = ('c_name', 'c_phone', 'c_gender', 'c_birth', 'c_add','c_code_valid')

        widgets = {
            'c_name': forms.TextInput(attrs={'class': 'form-control'}),
            'c_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'c_gender': forms.Select(attrs={'class': 'form-control'}),
            'c_add': forms.TextInput(attrs={'class': 'form-control'}),
            'c_code_valid': forms.TextInput(attrs={'class':'form-control'})
        }

        labels = {
            'c_name': '이름',
            'c_phone': '전화번호',
            'c_gender': '성별',
            'c_birth': '생년월일',
            'c_add': '주소',
            'c_code_valid': '자녀 학생코드(자녀 마이페이지에서 확인가능)'
        }
    # 자녀코드 확인
    def clean(self):
        cleaned_data = super().clean()
        code_valid = cleaned_data.get('c_code_valid')

        try:
            customer_tbl.objects.get(c_code=code_valid)
        except:
            self.add_error('c_code_valid', '존재하지 않는 학생 입니다.')


# 선생님
class teacher_Form(forms.ModelForm):
    class Meta:
        model = teacher_tbl
        fields = ['t_name','t_phone','t_gender','t_birth','t_add','t_file', 't_subject']
        widgets = {
            't_name': forms.TextInput(attrs={'class':'form-control'}),
            't_phone': forms.TextInput(attrs={'class':'form-control'}),
            't_gender': forms.Select(attrs={'class':'form-control'}),
            't_add': forms.TextInput(attrs={'class':'form-control'}),
            't_subject': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            't_name' : '이름',
            't_phone' : '전화번호',
            't_gender' : '성별',
            't_birth' : '생년월일',
            't_add' : '주소',
            't_file' : '사진',
            't_subject' : '과목',
        }





