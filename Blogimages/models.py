from django.db import models
from Posts.models import Post

# Create your models here.


class Blogimage(models.Model):
    Parent=models.ForeignKey(Post, related_name="Images", on_delete=models.CASCADE)
    Image=models.ImageField(blank=True)
    objects=models.Manager()
    def __str__(self):
        return 'image for post ' + str(self.ParentPost) 