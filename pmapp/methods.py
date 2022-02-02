from .models import *;

# add user defined methods here

# Check if registering user already exists
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


# returns a list which contains 2 lists - 1) list of submitted projects 2) Unique list classes
def get_submitted_students(tid):
    # Get all the projects assigned by that teacher
    all_submitted_projects = SubmitProject.objects.all()
    assigned_projects = Project.objects.filter(assigned_by=tid)

     # print(assigned_projects,'--------------')

    # Get single copies of the classes to which these projects are assigned to(set of class, since set stores unique values)
    classes_assigned_to = []
    for assigned in assigned_projects:
        classes_assigned_to.append(assigned.for_semsec)
    classes_assigned_to = list(set(classes_assigned_to))

    # print(classes_assigned_to,'---------------------')

    # Check from all submitted projects(ie from SubmitProject model) for the projects that are submitted to projects assigned by the currect teacher ,
    # submitted_projects give the list of submissions to that teacher

    submitted_projects = []
    for obj1 in all_submitted_projects:
        for obj2 in assigned_projects:
            if obj1.for_project_id.id == obj2.id:
                submitted_projects.append(obj1)

    # print(type(submitted_projects[0]),'---------')
    return [submitted_projects,classes_assigned_to]