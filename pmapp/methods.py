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

# write data to a new file 
# get graded projects of a specific class for a specific activity write details of student 
# student usn ,name, marks awarded

def create_report(tid):
    get_data = get_submitted_students(tid)
    classes_assigned_to = []
    # get class names
    for klas in get_data[1]:
        classes_assigned_to.append(klas.semsec)
    submitted_projects = get_data[0]
    # get projects which the teacher has graded
    graded_projects = []
    for submitted in submitted_projects:
        if submitted.grade is not None:
            graded_projects.append(submitted)
    # get all assigned projects sorted in ascending order of class assigned to
    all_assigned_projects = Project.objects.filter(assigned_by=tid).order_by('for_semsec')
    classwise_activities = {}
    # create a dictionary with all classes of that teacher as keys , and initialize it with an empty list which will contain the projects that the teacher assigns to that class 
    for klas in classes_assigned_to:
        classwise_activities[f'{klas}'] = []
    for klas in classes_assigned_to:
        for assigned in all_assigned_projects:
            if assigned.for_semsec.semsec == klas and assigned.assigned_by.tid == tid:
                classwise_activities[klas].append(assigned)

# create as many files for each class as the number of assigned projects for that class
    filepointers_to_be_closed = []
    for klas in classwise_activities:
       # print(klas,'----...----......-----.....-') to check if data is being passed till this line
        for assigned_projects in classwise_activities[klas]:
            fptr = open(f'reports/{assigned_projects.activity_name}{assigned_projects.for_subject.subj_code}class{klas}Report.xls','w')
            fptr.write(f'\t\t\t{assigned_projects.activity_name} ({assigned_projects.assigned_by.name} - {assigned_projects.for_subject.subj_name})\n\n')
            fptr.write('USN\t\tName\t\tGrade\n\n')
            filepointers_to_be_closed.append(fptr)
            for submitted in graded_projects:
                if submitted.for_project_id.for_semsec.semsec == klas and submitted.for_project_id.id == assigned_projects.id:
                    fptr.write(f'{submitted.submitted_by.usn}\t\t{submitted.submitted_by.name}\t\t{submitted.grade}\n')

# close all the opened file pointers
    for file in filepointers_to_be_closed:
        file.close()
    return classwise_activities

    
