from django.contrib import admin
from .models import Author
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
@admin.register(Author)
class AuthorAdmin(BaseUserAdmin):
    pass
