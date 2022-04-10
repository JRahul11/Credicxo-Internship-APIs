from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .groups import CustomGroups
# Importing inbuilt methods related to user authentication
from django.contrib.auth import authenticate, login
from api_app.models import User
# Importing the serializers
from auth_app.serializer import LoginSerializer, ValidateSerializer



# Login API (POST Request)
class LoginView(APIView):

    def post(self, request):
        data = request.data                                                     # Getting data from the API Request
        loginSerializer = LoginSerializer(data=data)                            # Validating the data using Serializer

        if loginSerializer.is_valid():                                          # Checking if user data is valid
            username = loginSerializer.data['username']
            password = loginSerializer.data['password']
            user = authenticate(username=username, password=password)           # Checking if a record exists with the given credentials

            if user is None:                                                    # No corresponding record found, return error
                return Response(
                    {
                        'status': 'Check Credentials'
                    }
                )
            else:
                login(request, user)                                            # Record found, hence login the user
                refresh = RefreshToken.for_user(user)                           # Generate a jwt refresh token for the user
                access = str(refresh.access_token)                              # Generate a jwt access token for the user
                response = Response(                                            # Return the access token with a success message
                    {
                        'status': 'User Logged In',
                        'refresh': str(refresh), 
                        'access': access
                    }
                )
                response.set_cookie(key='jwt', value=access, httponly=True)     # Set the access token as a cookie and respond
                return response

        else:
            return Response(                                                    # Error if user data is invalid
                {
                    'status': 'Error',
                    'message': loginSerializer.errors
                }
            )



# SignUp API (POST Request)
class SignUpView(APIView):

    def post(self, request):
        CustomGroups.createStudentGroup(self)
        CustomGroups.createTeacherGroup(self)
        CustomGroups.createSuperUserGroup(self)
        
        data = request.data                                                      # Getting data from the API Request
        signupSerializer = ValidateSerializer(data=data)                         # Validating the data using Serializer

        if signupSerializer.is_valid():
            username = signupSerializer.data['username']
            password = signupSerializer.data['password']
            user_type = signupSerializer.data['user_type']

            try:
                user = User.objects.create_user(username=username, password=password, user_type=user_type)  # Creating a new user
                CustomGroups.addUserToGroup(self, user, user_type)
                refresh = RefreshToken.for_user(user)                             # Generate a jwt refresh token for the user
                return Response(                                                  # Return the access token with a success message
                    {
                        'status': 'User Registered', 
                        'id': user.id, 
                        'refresh': str(refresh), 
                        'access': str(refresh.access_token)
                    }
                )
            except:
                user = User.objects.get(username=username)                         # If user already exists, return error
                return Response(
                    {
                        'status': 'Username Exists'
                    }
                )

        else:
            return Response(                                                       # Error if user data is invalid
                {
                    'status': 'Error',
                    'message': signupSerializer.errors
                }
            )



# ForgotPasswordView API (POST Request)
class ForgotPasswordView(APIView):

    def post(self, request):
        data = request.data                                                         # Getting data from the API Request
        forgotpasswordSerializer = ValidateSerializer(data=data)                    # Validating the data using Serializer

        if forgotpasswordSerializer.is_valid():
            username = forgotpasswordSerializer.data['username']
            password = forgotpasswordSerializer.data['password']
            user_type = forgotpasswordSerializer.data['user_type']

            try:
                user = User.objects.get(username=username, user_type=user_type)     # Fetch the user with the given username
                user.set_password(password)                                         # Set the password for the user
                user.save()
                return Response(                                                    # Return the access token with a success message
                    {
                        'status': 'Password Changed'
                    }
                )
            except:                                                                 # If user does not exist, return error
                return Response(
                    {
                        'status': 'Invalid Username or User Type'
                    }
                )

        else:                                                                       # Error if user data is invalid
            return Response(
                {
                    'status': 'Error',
                    'message': forgotpasswordSerializer.errors
                }
            )
