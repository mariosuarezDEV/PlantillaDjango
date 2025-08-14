from django.db import models
from django.contrib.auth.models import AbstractUser
from martor.models import MartorField
# Create your models here.


class User(AbstractUser):
    biografia = MartorField(blank=True, null=True, verbose_name="Biografía")
