from .models import *;

# add user defined methods here
def user_exists(id):
    s_obj = Student.objects.all()
    t_obj = Teacher.objects.all()
    student_id_list = []
    teacher_id_list = []
    for student in s_obj:
        student_id_list.append(student.usn)
    for teacher in t_obj:
        teacher_id_list.append(teacher.tid)   
    if id in student_id_list or id in teacher_id_list:
        return True
    else:
        return False

# # def login_user(login_id,loginpass):
#     student_obj = Student.objects.get(usn=login_id,password=loginpass)
#     teacher_obj = Teacher.objects.get(tid=login_id,password=loginpass)