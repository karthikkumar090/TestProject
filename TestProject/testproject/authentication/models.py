from django.contrib.auth.models import AbstractUser
from django.db import models

from testproject.models import BaseModel


USER_TYPE = (
    ("admin", "admin"),
    ("normal", "normal"),
)

class User(BaseModel, AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, default="")
    user_type = models.CharField(choices=USER_TYPE, default="admin", max_length=10)
