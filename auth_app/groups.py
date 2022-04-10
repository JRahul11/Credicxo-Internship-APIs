from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from api_app.models import User


class CustomGroups:

    # SuperUser Group
    def createSuperUserGroup(self):
        try:                                                                                # Check if the Group exists
            Group.objects.get(name='SuperUser')
        except:
            superUserGroup = Group.objects.create(name ='SuperUser')                        # Create SuperUser Group
            content_type = ContentType.objects.get_for_model(User)
            try:
                addPermission = Permission.objects.get(codename='add_user')
            except:
                addPermission = Permission.objects.create(name='Add User', codename='add_user', content_type = content_type)    # Add Permission for SuperUser
                superUserGroup.permissions.add(addPermission)                               # Append the Add Permission to SuperUser Group
            try:
                viewPermission = Permission.objects.get(codename='view_user')
            except:
                viewPermission = Permission.objects.create(name='View User', codename='view_user',content_type = content_type)  # View Permission for SuperUser
                superUserGroup.permissions.add(viewPermission)                              # Append the View Permission to SuperUser Group


    # Teacher Group
    def createTeacherGroup(self):
        try:                                                                                # Check if the Group exists
            Group.objects.get(name='Teacher')
        except:
            teacherGroup = Group.objects.create(name ='Teacher')                            # Create Teacher Group
            content_type = ContentType.objects.get_for_model(User)
            try:
                addPermission = Permission.objects.get(codename='add_student')
            except:
                addPermission = Permission.objects.create(name='Add Student', codename='add_student', content_type = content_type)    # Add Permission for Teacher
                teacherGroup.permissions.add(addPermission)                                 # Append the Add Permission to Teacher Group
            try:
                viewPermission = Permission.objects.get(codename='view_student')
            except:
                viewPermission = Permission.objects.create(name='View Student', codename='view_student',content_type = content_type)    # View Permission for Teacher
                teacherGroup.permissions.add(viewPermission)                                # Append the View Permission to Teacher Group


    # Student Group
    def createStudentGroup(self):
        try:                                                                                # Check if the Group exists
            Group.objects.get(name='Student')
        except:
            studentGroup = Group.objects.create(name ='Student')                            # Create Student Group
            content_type = ContentType.objects.get_for_model(User)
            try:
                viewPermission = Permission.objects.get(codename='view_profile')
            except:
                viewPermission = Permission.objects.create(name='View Profile', codename='view_profile',content_type = content_type)    # View Permission for Student
                studentGroup.permissions.add(viewPermission)                                # Append the View Permission to Student Group


    # Adding Users to Group
    # 1-> Student,    2-> Teacher,    3-> SuperUser
    def addUserToGroup(self, user, user_type):
        if user_type == 1:
            studentGroup = Group.objects.get(name ='Student')
            user.groups.add(studentGroup)
        elif user_type == 2:
            teacherGroup = Group.objects.get(name ='Teacher')
            user.groups.add(teacherGroup)
        elif user_type == 3:
            superUserGroup = Group.objects.get(name ='SuperUser')
            user.groups.add(superUserGroup)
