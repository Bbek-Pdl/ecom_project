from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid 
# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
        ) 
    phone_number = models.CharField(max_length=15,
                                    blank=True,
                                    null=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username