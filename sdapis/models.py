from django.db import models

class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_likes = models.BigIntegerField()
