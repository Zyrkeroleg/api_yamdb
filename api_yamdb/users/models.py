from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
   USER = 'user'
   ADMIN = 'admin'
   MODERATOR = 'moderator'
   user_type = [
      (USER, 'user'),
      (MODERATOR, 'moderator'),
      (ADMIN, 'admin'),
   ]
   bio = models.TextField(
        'Биография',
        blank=True,
   )
   role = models.CharField(
      max_length=20,
      choices=user_type,
      default=USER
   )
   