from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DnacControllers(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
