from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.


class User(AbstractUser):
    class Meta:
        ordering = ["id"]

    id = models.UUIDField(primary_key=True, default=uuid4)

    def get_absolute_url(self):
        return reverse('auth:user-detail', kwargs={'pk': self.pk})
