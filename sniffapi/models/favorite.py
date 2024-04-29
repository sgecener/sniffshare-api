from django.contrib.auth.models import User
from django.db import models

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    scent_post = models.ForeignKey("ScentPost", on_delete=models.CASCADE, related_name='favorite')

    def __str__(self):
        return f"{self.user.username} favorited {self.scent_post.title}"