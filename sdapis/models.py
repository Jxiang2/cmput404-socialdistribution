from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


def uuid_hex():
    return uuid.uuid4().hex

class Author(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    authorID = models.CharField(unique=True, default=uuid_hex, editable=False, max_length=100)
    github = models.CharField(max_length=200, blank=True)

    USERNAME_FIELD = 'email' # use email to login
    REQUIRED_FIELDS = ['username']

    def get_id(self):
        return settings.HOST_URL + "author/" + self.authorID

    def get_host(self):
        return settings.HOST_URL

    def get_type(self):
        return "author"