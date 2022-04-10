from django.urls import path
from .views import *

urlpatterns = [    

    path('addUser/', AddUser.as_view()),                        # Add User Endpoint

    path('viewUser/', ViewUser.as_view()),                      # View User Endpoint
]
