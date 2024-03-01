from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(null=True, unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']
# Create your models here.
