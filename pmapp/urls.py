from django.urls import path
from pmapp import views

urlpatterns = [
    path('',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('registerStudent/',views.registerStudent,name="registerStudent"),
    path('registerTeacher/',views.registerTeacher,name="registerTeacher"),
    # Student Related URL mapping
    path('profileStudent/<str:usn>/',views.profileStudent,name="profileStudent"),
    path('handInProject/<str:usn>/<int:pid>/',views.handInProject,name="handInProject"),
    path('profileStudent/<str:usn>/submitted/<int:sid>/update/',views.updateProjectStudent,name="updateProjectStudent"),
    path('profileStudent/<str:usn>/submitted/<int:sid>/delete/',views.deleteProjectStudent,name="deleteProjectStudent"),
    path('profileStudent/<str:usn>/submitted/',views.submitted,name="submitted"),
    path('profileStudent/<str:usn>/graded/',views.gradedStudent,name="gradedStudent"),
    # Teacher related URL mapping
    path('profileTeacher/<str:tid>/',views.profileTeacher,name="profileTeacher"),
    path('profileTeacher/<str:tid>/assigned/<int:pid>/update/',views.updateProject,name="updateProject"),
    path('profileTeacher/<str:tid>/assigned/<int:pid>/delete/',views.deleteProject,name="deleteProject"),
    path('profileTeacher/<str:tid>/assigned/',views.assigned,name="assigned"),
    path('profileTeacher/<str:tid>/submissions/',views.submissions,name="submissions"),
    path('profileTeacher/<str:tid>/graded/',views.graded,name="graded"),
    path('addProject/<str:tid>/',views.addProject,name="addProject"),
    
]