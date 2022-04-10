from auth_app.groups import CustomGroups
from auth_app.serializer import ValidateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# Importing the Custom User Model
from api_app.models import User



# Add User Class
class AddUser(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication


    # Create User Record if doesnt exist
    def createNewUser(self, username, password, user_type):
        try:                                                                                # Check if user already exists
            User.objects.get(username=username)
            return 'User Exists'
        except:                                                                             # Create a new user if doesnt exist
            new_user = User.objects.create_user(username=username, password=password, user_type=user_type)
            CustomGroups.addUserToGroup(self, new_user, user_type)
            return 'User Added'


    # POST Request
    def post(self, request):
        username = request.user                                                             # Get the user from the request
        user = User.objects.get(username=username)                                          # Get the user record

        if user.groups.filter(name='SuperUser'):                                            # Check if user is a SuperUser
            data = request.data                                                             # Get the data from the request
            addUserSerializer = ValidateSerializer(data=data)                               # Data Validation using Serializer
            if addUserSerializer.is_valid():
                username = addUserSerializer.data['username']
                password = addUserSerializer.data['password']
                user_type = addUserSerializer.data['user_type']
                status = self.createNewUser(username, password, user_type)                  # Call createNewUser for new user check
                return Response(
                    {
                        'status': status,
                    }
                )

        elif user.groups.filter(name='Teacher'):                                            # Check if user is a Teacher
            data = request.data                                                             # Get the data from the request
            addUserSerializer = ValidateSerializer(data=data)                               # Data Validation using Serializer
            if addUserSerializer.is_valid():
                username = addUserSerializer.data['username']
                password = addUserSerializer.data['password']
                user_type = addUserSerializer.data['user_type']

                if user_type == 1:                                                          # Teacher can only add Students
                    status = self.createNewUser(username, password, user_type)              # Call createNewUser for new user check
                    return Response(
                        {
                            'status': status,
                        }
                    )
                else:
                    return Response(                                                        # Error if new user is SuperUser or Teacher
                        {
                            'status': 'Error',
                            'message': 'Insufficient Permissions to perform the request'
                        }
                    )

        elif user.groups.filter(name='Student'):                                            # Check if user is a Student
            return Response(
                {                                                                           # Error because Students cannot add Users
                    'status': 'Error',
                    'message': 'Insufficient Permissions to perform the request'
                }
            )



# View User Class
class ViewUser(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication


    def createUserJSON(self, user):                                                               # Create a JSON for the user data
        if user.user_type == 1:
            user_type = 'Student'
        elif user.user_type == 2:
            user_type = 'Teacher'
        elif user.user_type == 3:
            user_type = 'SuperUser'
        temp = {
            'id': user.id,
            'username': user.username,
            'user_type': user_type
        }
        return temp


    # GET Request
    def get(self, request):
        response = []                                                                       # Create a list to store the user data
        username = request.user                                                             # Get the user from the request
        user = User.objects.get(username=username)                                          # Get the user record

        if user.groups.filter(name='SuperUser'):                                            # Check if user is a SuperUser
            users = User.objects.all()                                                      # SuperUser can view all the Users
            for user in users:
                response.append(self.createUserJSON(user))                                  # Append the user JSON to the list
            return Response(response)
        elif user.groups.filter(name='Teacher'):                                            # Check if user is a Teacher
            users = User.objects.filter(user_type=1)                                        # Teacher can view all the Students
            for user in users:
                response.append(self.createUserJSON(user))                                  # Append the user JSON to the list
            return Response(response)
        elif user.groups.filter(name='Student'):                                            # Check if user is a Student
            response.append(self.createUserJSON(user))                                      # Append the user JSON to the list
            return Response(response)
