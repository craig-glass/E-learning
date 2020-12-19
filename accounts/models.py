from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, null=False)
    phone_number = models.CharField(max_length=20)
    term_address = models.CharField(max_length=150)
    is_student = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']
