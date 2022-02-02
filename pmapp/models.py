from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.urls import reverse
 
# Create your models here.
class Department(models.Model):
    DEPARTMENT_ID = (
        ('CS','CS'),('IS','IS'),('ECE','ECE'),('IEM','IEM'),('CIV','CIV'),('MECH','MECH'),('EEE','EEE'))   
    DEPARTMENT_NAME = (
        ('Computer Science And Engineering','Computer Science And Engineering'),
        ('Information Sciecne And Engineering','Information Sciecne And Engineering'),
        ('Electronics And Communication','Electronics And Communication'),
        ('Industrial Engineering And Management','Industrial Engineering And Management'),
        ('Civil Engineering','Civil Engineering'),
        ('Mechanical Engineering','Mechanical Engineering'),
        ('Electronics And Electrical Engineering','Electronics And Electrical Engineering')
    )
    d_id = models.CharField(max_length=100, primary_key=True, choices=DEPARTMENT_ID)
    d_name = models.CharField(max_length=100, choices=DEPARTMENT_NAME)
    class Meta:
        db_table = 'DEPARTMENT'   
    def __str__(self):
        return self.d_id


class Class_Section(models.Model):
    semsec = models.CharField(max_length=2,primary_key=True,default='5A')
    semester = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(8)],default='5')
    section = models.CharField(max_length=1,default='A')
    class Meta:
        db_table = 'Class'
    def __str__(self):
        return self.semsec


class Student(models.Model):
    usn = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.DecimalField(max_digits=10,decimal_places=0,blank=True,null=True)
    password = models.CharField(max_length=100,default='0000')
    branch = models.ForeignKey(Department,on_delete=models.CASCADE,default='CS')
    semsec = models.ForeignKey(Class_Section,on_delete=models.CASCADE,default="5A")
    class Meta:
        db_table = 'STUDENT'
    def __str__(self):
        return self.usn
    def get_absolute_url(self):
        return f'/profileStudent/{self.usn}/'


class Teacher(models.Model):
    tid = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.DecimalField(max_digits=10,decimal_places=0,blank=True,null=True)
    password = models.CharField(max_length=100,default='0000')
    branch = models.ForeignKey(Department,on_delete=models.CASCADE)
    class Meta:
        db_table = 'TEACHER'
    def __str__(self):
        return self.tid

    def get_absolute_url(self):
        return f'/profileTeacher/{self.tid}/'

class Subject(models.Model):
    CREDITS = ((1,1),(2,2),(3,3),(4,4))
    SEMESTER = ((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8))
    subj_code = models.CharField(max_length=8,primary_key=True)
    subj_name = models.CharField(max_length=100)
    semester = models.IntegerField(default=1,choices=SEMESTER)
    credits = models.IntegerField(default=1,choices=CREDITS)
    branch = models.ForeignKey(Department,on_delete=models.CASCADE,default="CS")
    class Meta:
        db_table = 'SUBJECT'
    def __str__(self):
        return self.subj_code

class Project(models.Model):
    activity_name = models.CharField(max_length=100)
    activity_description = models.TextField(help_text="Provide Activity Description(if any)", blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True,blank=True)
    deadline = models.DateTimeField(null=True)
    for_semsec = models.ForeignKey(Class_Section,on_delete=models.CASCADE)
    for_subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(Teacher,on_delete=models.CASCADE,default='CS100')
    class Meta:
        db_table = 'PROJECTS'
    def __str__(self):
        return self.activity_name + ' ' + str(self.assigned_by) + ' ' + str(self.for_subject)

class SubmitProject(models.Model):
    project_title = models.CharField(max_length=100,blank=True,null=True)
    source_url = models.URLField(max_length=400,null=True,blank=True)
    grade = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],null=True,blank=True)
    submitted_by = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
    submisstion_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    for_project_id = models.ForeignKey(Project,on_delete=models.CASCADE, default=1)
    class Meta:
        db_table = 'SUBMITPROJECT'
    def __str__(self):
        return self.project_title
