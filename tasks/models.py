from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, name, password=None, **extra_fields):
        """ Creates a new user"""

        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'name'

    class Meta:
        db_table = "api_user"
        ordering = ["-id"]


class Task(models.Model):
    name = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        db_table = 'api_tasks'
        ordering = ['-created_at']
