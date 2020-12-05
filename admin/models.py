from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class customer_tbl(models.Model):
    user = models.OneToOneField(User, null=True ,on_delete = models.CASCADE)
    c_no = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=10, null=True, blank=True)
    c_phone = models.CharField(max_length=20, null=True, blank=True)
    c_gender = models.CharField(max_length=10, choices=(('남', '남'), ('여', '여')), null=True, blank=True)
    c_join = models.DateField(auto_now_add=True, null=True)
    c_birth = models.DateField(null=True, blank=True)
    c_code = models.CharField(max_length=6, null=True, blank=True)
    c_add = models.CharField(max_length=50, null=True, blank=True)
    c_school = models.CharField(max_length=50, null=True, blank=True)
    c_state = models.BooleanField(null=True, blank=True)
    # 수정
    c_out = models.DateField(null=True, blank=True)
    # 학부모 일 경우 자식의 학생 코드
    c_code_valid = models.CharField(max_length=6, null=True)
    # 인증과정
    c_auth = models.CharField(max_length=8, null=True)

@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            teacher_tbl.objects.create(user=instance)
        else:
            customer_tbl.objects.create(user=instance)


class teacher_tbl(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    t_no = models.AutoField(primary_key=True)
    t_name = models.CharField(max_length=10 , null=True, blank=True)
    t_phone = models.CharField(max_length=20, null=True, blank=True)
    t_gender = models.CharField(max_length=10, null=True, blank=True, choices=(('남','남'),('여','여')))

    # 과목 선택 Choice
    subject_choice = (('수학', '수학'), ('영어', '영어'))
    t_subject = models.CharField(max_length=10, null=True, blank=True, choices=subject_choice)
    t_birth = models.DateField(null=True, blank=True)
    t_state = models.BooleanField(null=True)
    t_add = models.CharField(max_length=50, null=True)
    t_join = models.DateField(auto_now_add=True)
    # 사진이 저장될 때의 경로 -> upload_to
    t_file = models.ImageField(upload_to='teacher/', blank=True, null=True)
    t_out = models.DateField(null=True)
    t_text = models.CharField(max_length=500, null=True)
    # 인증과정때 필요한 필드
    c_auth = models.CharField(max_length=8, null=True)


    # 객체의 이름이 보이게(강의 등록에서 이용)
    def __str__(self):
        return self.t_name

class lecture_tbl(models.Model):
    l_no = models.AutoField(primary_key=True)
    # 강의명
    l_name = models.CharField(max_length=200, null=True, blank=True)
    # 정원
    l_totalnum = models.IntegerField()
    # 강의 기간 선택
    term_choice = ((1,'1개월'),(2,'2개월'),(3,'3개월'))
    # 기간
    l_term = models.IntegerField(choices = term_choice)
    # 강의료
    l_pay = models.IntegerField()
    # 시작일
    l_startdate = models.DateField()
    # 선생님 번호(외래키)
    t_no = models.ForeignKey(teacher_tbl , on_delete=models.CASCADE)
    # 강의 커리큘럼 설명
    l_desc = models.CharField(max_length=500, null=True)
    # 이미지
    l_img = models.ImageField(upload_to='lecture/%Y/%m/%d', null=True)

    # 부서 Choice
    dept_choice = (('중등' , '중등'), ('고등', '고등'))
    l_dept = models.CharField(max_length=20, choices = dept_choice)

    # 학년 Choice ( 콤보박스에는 *학년 이라고 표시되지만 실제 저장되는 데이터는 숫자만 저장 )
    class_choice = (('1', '1학년'), ('2' ,'2학년'), ('3' ,'3학년'))
    l_class = models.CharField(max_length=10, choices = class_choice)

class training_tbl(models.Model):
    tr_no = models.AutoField(primary_key=True)
    tr_date = models.DateField(auto_now_add=True)
    l_no = models.ForeignKey(lecture_tbl, on_delete=models.CASCADE)
    c_no = models.ForeignKey(customer_tbl, on_delete=models.CASCADE)

# 자주하는 질문
class faq_tbl(models.Model):
    faq_no = models.AutoField(primary_key=True)
    faq_question = models.TextField()
    faq_answer = models.TextField()
    faq_date = models.DateTimeField()

# 공지사항
class notice_tbl(models.Model):
    notice_no = models.AutoField(primary_key=True)
    notice_title = models.CharField(max_length=200)
    n_writer = models.CharField(max_length=20)
    notice_date = models.DateTimeField()
    subject_choice = (('선생님', '선생님'), ('전체', '전체'))
    notice_target = models.CharField(max_length=20, choices=subject_choice)
    notice_content = models.TextField()

# 온라인 자료
class online_tbl(models.Model):
    on_no = models.AutoField(primary_key=True)
    on_title = models.CharField(max_length=200)
    l_no = models.ForeignKey(lecture_tbl, on_delete=models.CASCADE)
    on_content = models.TextField()
    on_date = models.DateTimeField()
    on_div = models.CharField(max_length=20)
    on_file = models.FileField(upload_to='online/',null=True,blank=True)

# 출결
class attendance_tbl(models.Model):
    at_no = models.AutoField(primary_key=True)
    attendance = models.CharField(max_length=20)
    tr_no = models.ForeignKey(training_tbl, on_delete=models.CASCADE)
    at_date = models.DateField()


##################### 시험 추가 #########################################

# 강의에서 l_no를 받은 test_tbl
class test_tbl(models.Model):
    # 기본키(일련번호)
    te_no = models.AutoField(primary_key=True)
    # 시험명
    te_name = models.CharField(max_length=200, null=True, blank=True)
    # 시험 등록일
    te_join = models.DateField(auto_now_add=True)
    # 외래키(강의 번호) - 강의 테이블이 삭제되었을 시 같이 삭제.
    l_no = models.ForeignKey(lecture_tbl, on_delete=models.CASCADE)

# 시험문제 - 상세(시험의 문제와 객관식 정답등을 저장) test_detail
class test_detail_tbl(models.Model):
    # 기본키(일련번호)
    td_no = models.AutoField(primary_key=True)
    # 외래키(시험 테이블(test_tbl)) - 시험 객체 삭제시 자동으로 같이 삭제
    te_no = models.ForeignKey(test_tbl, on_delete=models.CASCADE)
    # 문제 번호
    td_question_no = models.IntegerField()
    # 문제
    td_question = models.CharField(max_length=1000, null=True, blank=True)
    # 객관식 1번
    td_choice_1 = models.CharField(max_length=500, null=True, blank=True)
    # 객관식 2번
    td_choice_2 = models.CharField(max_length=500, null=True, blank=True)
    # 객관식 3번
    td_choice_3 = models.CharField(max_length=500, null=True, blank=True)
    # 객관식 4번
    td_choice_4 = models.CharField(max_length=500, null=True, blank=True)
    # 정답
    td_answer = models.IntegerField(null=True, blank=True)

# 시험 신청(training_tbl과 test_tbl간의 관계에서 만들어지는 테이블)
class test_apply(models.Model):
    # 기본키(일련번호)
    ta_no = models.AutoField(primary_key=True)
    # 시험본 날짜
    ta_date = models.DateField(auto_now_add=True)
    # 외래키(시험테이블) - 시험이 지워지면 자동으로 삭제
    te_no = models.ForeignKey(test_tbl, on_delete=models.CASCADE)
    # 외래키(수강테이블(training_tbl))
    tr_no = models.ForeignKey(training_tbl, on_delete=models.CASCADE)
    # 점수
    te_score = models.IntegerField()

# 상담
class consult_tbl(models.Model):
    cu_no = models.AutoField(primary_key=True)
    cu_cust = models.CharField(max_length=20)
    cu_join_time = models.DateTimeField(null=True)
    cu_res_time = models.DateTimeField(null=True)
    cu_content = models.TextField(null=True,blank=True)
    cu_state = models.CharField(max_length=10, null=True, blank=True)
    c_no = models.ForeignKey(customer_tbl, on_delete=models.CASCADE)
    t_no = models.ForeignKey(teacher_tbl, on_delete=models.CASCADE)
    cu_text = models.TextField(null=True,blank=True)
    cu_student = models.CharField(max_length=100, null=True, blank=True)

    # 권한 생성
    class Meta:
        permissions = [
            ('can_view_consult','Can View Consult')
        ]


# 사용자 페이지 이미지(학원 소개)
class userpage_tbl(models.Model):
    page_img_main = models.ImageField(upload_to='userpage/', null=True, blank=True)
    page_img_sub1 = models.ImageField(upload_to='userpage/', null=True, blank=True)
    page_img_sub2 = models.ImageField(upload_to='userpage/', null=True, blank=True)