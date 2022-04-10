from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):                                           # Custom User Model
    USER_TYPE_CHOICES = (                                           # User Roles
        (1, 'Student'),
        (2, 'Teacher'),
        (3, 'Superuser')
    )

    # Custom Model Field
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    
    USERNAME_FIELD  = 'username'                                    
    REQUIRED_FIELDS = ['password', 'user_type']
    
    def __str__(self):
        return self.username