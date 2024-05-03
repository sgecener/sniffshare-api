from django.contrib.auth.models import User
from django.db import models

class ScentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)