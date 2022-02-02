from asyncio.windows_events import NULL
from multiprocessing import context
from turtle import update
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .methods import *

# Create your views here.

# ----------------------------------------------
# Student related views and logic here on
# ----------------------------------------------

def profileStudent(request, usn):
    student_obj = Student.objects.get(usn=usn)
    project_objs = Project.objects.filter(for_semsec = student_obj.semsec)
    submitted_objs = SubmitProject.objects.filter(submitted_by=usn)
    submitted_projects = []
    # Display only those Projects which have not been submitted by the student
    for submmitted_project in submitted_objs:
        submitted_projects.append(submmitted_project.for_project_id)
    # The 2 querysets are type caseted to set datatype this gives us the ability to treat the querysets as sets and perform set functions(union,intersection,minus..) on them, here we use minus(-) function
    display_projects = set(project_objs)-set(submitted_projects)
    context = {
        'student': student_obj,
        'projects': display_projects,
        
    }
    return render(request, 'profileStudent.html', context)

def handInProject(request, usn, pid):
    project_obj = Project.objects.get(id=pid)
    student_obj = Student.objects.get(usn=usn)
    if request.method == 'GET':
        project_title = request.GET.get('project_title')
        project_url = request.GET.get('project_url')
        handIn_obj = SubmitProject(project_title=project_title,source_url=project_url,submitted_by=student_obj,for_project_id=project_obj)
        handIn_obj.save()
        messages.success(request,f'{project_obj.activity_name} handed in Successfully')
        return redirect(student_obj)

def submitted(request,usn):
    submitted_objs = SubmitProject.objects.filter(submitted_by=usn)
    submitted_but_not_graded_projects = []
    for obj in submitted_objs:
        if obj.grade is None:
            submitted_but_not_graded_projects.append(obj)
    context = {
         'submitted_projects':submitted_but_not_graded_projects,
         'usn':usn
        }
    return render(request,'submitted.html',context)

def updateProjectStudent(request,usn,sid):
    update_obj = SubmitProject.objects.get(id=sid)
    context = {
        'usn':usn,
        'update_project':update_obj
    }
    if request.method == 'POST':
        project_title = request.POST.get('project_title')
        source_url = request.POST.get('source_url')
        SubmitProject.objects.filter(id=sid).update(project_title=project_title,source_url=source_url)
        messages.success(request,f'Submission for {update_obj.for_project_id.activity_name} Successfully Updated')
        submitted_projects = SubmitProject.objects.filter(submitted_by=usn)
        submitted_but_not_graded_projects = []
        for obj in submitted_projects:
            if obj.grade is None:
                submitted_but_not_graded_projects.append(obj)
        context = {
            'usn':usn,
            'submitted_projects':submitted_but_not_graded_projects
        }
        return render(request,'submitted.html',context)
    return render(request,'updateProjectStudent.html',context)

def deleteProjectStudent(request,usn,sid):
    delete_obj = SubmitProject.objects.get(id=sid)
    project_title = delete_obj.project_title
    delete_obj.delete()
    submitted_projects = SubmitProject.objects.filter(submitted_by=usn)
    submitted_but_not_graded_projects = []
    for obj in submitted_projects:
        if obj.grade is None:
            submitted_but_not_graded_projects.append(obj)
    context = {
        'usn':usn,
        'submitted_projects':submitted_but_not_graded_projects
    }
    messages.success(request,f'{project_title} Deleted')
    return render(request, 'submitted.html', context)

def gradedStudent(request,usn):
    submitted = SubmitProject.objects.filter(submitted_by=usn)
    graded_projects = []
    for obj in submitted:
        if obj.grade is not None:
            graded_projects.append(obj)
    context={
        'usn':usn,
        'graded_projects':graded_projects,
    }
    return render(request,'gradedStudent.html',context)

# ----------------------------------------------
# Teacher Related Views and logic here on
# ----------------------------------------------

def profileTeacher(request, tid):
    teacher_obj = Teacher.objects.get(tid=tid)
    subject_obj = Subject.objects.all()
    class_obj = Class_Section.objects.all()
    context = {
        'teacher': teacher_obj,
        'subjects': subject_obj,
        'for_class': class_obj,
    }
    return render(request, 'profileTeacher.html', context)

def addProject(request,tid):
    if request.method == 'GET':
        activity_name = request.GET.get('activity_name')
        for_subject = request.GET.get('for_subject')
        deadline = request.GET.get('deadline') 
        if request.GET.get('activity_description'):
            activity_description = request.GET.get('activity_description')
        else:
            activity_description = 'No description'
        assign_to = request.GET.get('assign_to')
        # reference to existing Teacher from database who assigns the project/assignment
        teacher_obj = Teacher.objects.get(tid=tid)
        # reference to existing subject object from database to which assignment has to be assigned
        subj_obj = Subject.objects.get(subj_code=for_subject)
        # referece to existing class object from database to which assignment has to be assigned
        to_class = Class_Section.objects.get(semsec=assign_to)
        # create a new project object and save to database
        project_obj = Project(activity_name=activity_name, for_subject=subj_obj,activity_description=activity_description,
                              deadline=deadline, for_semsec=to_class, assigned_by=teacher_obj)
        project_obj.save()
        messages.success(request,'Assignment added')
        return redirect(teacher_obj)

def deleteProject(request,tid,pid):
    delete_obj = Project.objects.get(id=pid)
    activity_name = delete_obj.activity_name
    delete_obj.delete()
    assigned_projects = Project.objects.filter(assigned_by=tid)
    context = {
        'teacher_id' : tid,
        'assigned_projects':assigned_projects
    }
    messages.success(request,f'{activity_name} Deleted')
    return render(request, 'assigned.html', context)

def assigned(request, tid):
    assigned_projects = Project.objects.filter(assigned_by=tid)
    context = {
        'teacher_id' : tid,
        'assigned_projects':assigned_projects
    }
    return render(request, 'assigned.html', context)

def updateProject(request,tid,pid):
    update_obj = Project.objects.get(id=pid)
    context ={
        'teacher_id':tid,
        'update_project':update_obj,
        }
    if request.method == 'POST':
        activity_description = request.POST.get('activity_description')
        deadline = request.POST.get('deadline')
        Project.objects.filter(id=pid).update(activity_description=activity_description,deadline=deadline)
        messages.success(request,f'{update_obj.activity_name} Updated for {update_obj.for_semsec}')
        assigned_projects = Project.objects.filter(assigned_by=tid)
        context = {
            'teacher_id' : tid,
            'assigned_projects':assigned_projects
        }
        return render(request, 'assigned.html', context)   
    return render(request,'updateProject.html',context)

def submissions(request,tid):
    get_user = get_submitted_students(tid)
    classes_assigned_to =get_user[1]
    submitted_projects = get_user[0]
    non_graded_submissions = []
    for obj in submitted_projects:
        if obj.grade is None:
            non_graded_submissions.append(obj)
    context = {
            'teacher_id':tid,
            'classes':classes_assigned_to,
            'submitted_projects':non_graded_submissions,
        }
    if request.method == 'POST':
        grade = request.POST.get('grade')
        sid = request.POST.get('sid')
        SubmitProject.objects.filter(id=sid).update(grade=grade)
        messages.success(request,"Graded")   
        return render(request,'submissions.html',context)    
    return render(request,'submissions.html',context)

def graded(request,tid):
    get_user = get_submitted_students(tid)
    classes_asigned_to = get_user[1]
    submitted_projects = get_user[0]
    graded_projects = []
    for obj in submitted_projects:
        if obj.grade is not None:
            graded_projects.append(obj)
    context = {
        'classes':classes_asigned_to,
        'teacher_id':tid,
        'submitted_projects': graded_projects
    }
    if request.method == 'POST':
        grade = request.POST.get('grade')
        sid = request.POST.get('sid')
        SubmitProject.objects.filter(id=sid).update(grade=grade)
    return render(request,'graded.html',context)

# ---------------------------------------------------------------------
# Registration Views and Logic to store a new user to database Here on
# ---------------------------------------------------------------------

def register(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        tid = request.POST.get('tid')
        name = request.POST.get('name')
        email = request.POST.get('email')
        branch = request.POST.get('branch')
        # create department object reference to pass to Student/Teacher object
        dept_obj = Department.objects.get(d_id=branch)
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        # check if registering user exists
        if user_exists(usn) or user_exists(tid):
            messages.error(request, 'User already exists!')
            return redirect('register')
        # if user enters phone collect it, else store null
        if phone:
            phone = phone
        else:
            phone = NULL

        # if registering user is Student then store to student database
        if usn:
            semester = request.POST.get('semester')
            section = request.POST.get('section')
            semsec = str(semester + section)
            # create class object reference to pass to Student object
            class_obj = Class_Section.objects.get(semsec=semsec)
            # pass the above references and create a student entry and save to database
            student_obj = Student(usn=usn, name=name, email=email, phone=phone,
                                  password=password, branch=dept_obj, semsec=class_obj)
            student_obj.save()
            if Student.objects.get(usn=usn):
                messages.success(request, f'{usn} Registered Successfully')
                return redirect('login')
            else:
                messages.error(request, "Unable to save user")
                return redirect('login')

        # else registering user is Teacher , create teacher entry and save to database
        else:
            teacher_obj = Teacher(
                tid=tid, name=name, email=email, phone=phone, password=password, branch=dept_obj)
            teacher_obj.save()
            if Teacher.objects.get(tid=tid):
                messages.success(request, f'{tid} Registered Successfully')
                return redirect('login')
            else:
                messages.error(request, "Unable to save user")
                return redirect('login')

    return render(request, 'register.html')

def registerStudent(request):
    depts = Department.objects.all()
    context = {'departments': depts}
    return render(request, 'registerStudent.html', context)

def registerTeacher(request):
    depts = Department.objects.all()
    context = {'departments': depts}
    return render(request, 'registerTeacher.html', context)

# ----------------------------------------------
# LOGIN logic and view
# ----------------------------------------------

def login(request):
    if request.method == 'POST':
        login_id = request.POST['login_id']
        loginpass = request.POST['loginpass']
        student = request.POST.get('student')
        teacher = request.POST.get('teacher')
        if student:
            try:
                student_obj = Student.objects.get(
                    usn=login_id, password=loginpass)
                return redirect(student_obj, permanent=True)
            except:
                messages.error(request, "Student USN or Password Invalid")
                return redirect('login')
        elif teacher:
            try:
                teacher_obj = Teacher.objects.get(
                    tid=login_id, password=loginpass)
                return redirect(teacher_obj, permanent=True)
            except:
                messages.error(request, "Teacher ID or password Invalid")
                return redirect('login')
        else:
            messages.error(request, "INVALID USER")
            return redirect('login')

    return render(request, 'login.html')