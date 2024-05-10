from django.contrib.auth.models import User
from django.db import models

class ScentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)

    @property
    def favorite_posts(self):
        return self.__favorite_posts
    
    @favorite_posts.setter
    def favorite_posts(self, value): 
        self.__favorite_posts = value
        