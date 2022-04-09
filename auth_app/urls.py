from django.urls import path

# Import JWT Inbuilt Classes
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from .views import *

urlpatterns = [
    
    # Authentication URLs
    path('login/', LoginView.as_view()),                            # Login API
    path('signup/', SignUpView.as_view()),                          # SignUp API
    path('forgotpassword/', ForgotPasswordView.as_view()),          # Forgot Password API
    
    # JWT URLs
    path('token/', TokenObtainPairView.as_view()),                  # Generate JWT Token
    path('token/refresh/', TokenRefreshView.as_view()),             # Refresh JWT Token  
]
