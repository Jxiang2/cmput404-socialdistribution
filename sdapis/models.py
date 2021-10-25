from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField
from django.contrib.postgres.fields import ArrayField
from django.db.models.deletion import CASCADE
from django.conf import settings
import uuid


HOST_NAME = settings.HOST_NAME

def uuid_hex():
    return uuid.uuid4().hex

class Author(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    author_id = models.CharField(unique=True, default=uuid_hex, editable=False, max_length=100)
    github = models.CharField(max_length=200, blank=True)
    profile_image = models.CharField(max_length=500, null=True)
    USERNAME_FIELD = 'email' # use email to login
    REQUIRED_FIELDS = ['username']

    def get_id(self):
        return HOST_NAME + "/api" +"/author/" + self.author_id

    def get_host(self):
        return HOST_NAME

    def get_type(self):
        return "author"

class Post(models.Model):
    title = models.CharField(max_length=200)
    id = models.CharField(primary_key=True, default=uuid_hex, unique=True, max_length=100)

    source = models.URLField(max_length=200, null=True)
    origin = models.URLField(max_length=200, null=True)
    description = models.TextField(default= "description of the post")
    contentType = models.CharField(max_length=20, default="text/plain")
    content = models.TextField()
    # author 1 <-> * post
    author_id = models.CharField(max_length=100, default="no author")
    comment_list = ArrayField(models.JSONField(), default=list)

    PUBLIC = 'PUBLIC'
    FRIENDS = 'FRIEND'

    STATUS_CHOICES = [
        (PUBLIC, 'public'),
        (FRIENDS, 'friend'),
    ]
    visibility = models.CharField(choices=STATUS_CHOICES, default=PUBLIC, max_length=6)
    category = CharField(max_length=200, default="Web Tutorial")
    
    #category will be added in the next part!
    #visibility will be adde in the next part!

    count = models.IntegerField(default=0)
    published = models.DateTimeField(auto_now_add=True)
    unlisted = models.BooleanField(default=False)
    
    def get_post_id(self):
        return "{}/api/author/{}/posts/{}".format(HOST_NAME, self.author_id, str(self.id))

    def get_type(self):
        return "post"

class Comment(models.Model):
    comment = models.TextField()
    contentType = models.CharField(max_length=20, default="text/plain")
    published = models.DateTimeField(auto_now_add=True)
    comment_id = models.UUIDField(primary_key=True, default=uuid_hex, unique=True)
    # author 1 <-> * comment
    comment_author = models.ForeignKey(Author, on_delete=CASCADE)
    # post 1 <-> * comment
    post = models.ForeignKey(Post, on_delete=CASCADE)
    # def get_id(self):
    # return settings.HOST_URL + "author/" + self.authorID

    def get_comment_id(self):
        return "{}/api/author/{}/posts/{}/comments/{}".format(HOST_NAME, self.comment_author.author_id, str(self.post_of_comment.post_id),str(self.comment_id))

    def get_type(self):
        return "comment"

class Follow(models.Model):
    # author2 follows author1
    author1 = models.CharField(max_length=50)
    author2 = models.CharField(max_length=50)

class Inbox(models.Model):
    author_id = models.CharField(max_length=40, unique=True)
    items = ArrayField(models.JSONField(), default=list) # array of objects

    def get_author(self):
        return settings.HOST_NAME + "author/" + self.author_id

    def get_type(self):
        return "inbox"

class Node(models.Model):
    host = models.CharField(max_length=150)