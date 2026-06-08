from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


class User(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN','Admin'),
        ('LIBRARIAN','Librarian'),
        ('USER','User'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    password_setup_token = models.UUIDField(
        default=uuid4,
        null=True,
        blank=True,
        unique=True
    )

    def __str__(self):
        return self.username
    


