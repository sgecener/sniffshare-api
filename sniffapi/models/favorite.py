
from django.db import models

class Favorite(models.Model):
    scent_user = models.ForeignKey("ScentUser", on_delete=models.CASCADE, related_name='favorites')
    scent_post = models.ForeignKey("ScentPost", on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f"{self.user.username} favorited {self.scent_post.title}"