
from django.db import models

class ScentTag(models.Model):
    scent_post = models.ForeignKey("ScentPost", on_delete=models.CASCADE, related_name='scent_tag')
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name='scent_tag')

    def __str__(self):
        return f"{self.tag.name} for {self.scent_post.title}"