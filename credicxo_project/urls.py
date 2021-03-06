from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from api_app.views import Welcome

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Base URL
    path('', Welcome.as_view()),
    
    # Authentication URLs
    path('auth/', include('auth_app.urls')),
    
    # Main API URLs
    path('api/', include('api_app.urls')),
]
