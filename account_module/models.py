from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


#
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.get_full_name()
