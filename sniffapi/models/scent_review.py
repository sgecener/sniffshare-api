from django.contrib.auth.models import User
from django.db import models

class ScentReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scent_reviews')
    scent_post = models.ForeignKey("ScentPost", on_delete=models.CASCADE, related_name='scent_reviews')
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.scent_post.title}"