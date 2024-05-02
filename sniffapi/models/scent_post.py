from django.contrib.auth.models import User
from django.db import models
from .category import Category
from .tag import Tag
from .scent_tag import ScentTag


class ScentPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scent_posts')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='scent_posts')
    tags = models.ManyToManyField(Tag, through= ScentTag, related_name='scent_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title