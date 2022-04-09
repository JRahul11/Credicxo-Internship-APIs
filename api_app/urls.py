from django.urls import path
from .views import *

urlpatterns = [
    
    # Base URL
    path('', Welcome.as_view()),
    
    # Main APIs
    # path('api/', include('api_app.urls')),
]
