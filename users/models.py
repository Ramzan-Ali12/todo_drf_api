from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import uuid

# Common model
class CommonModels(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use the full app label for the ForeignKey references
    created_by = models.ForeignKey('users.CustomUser', related_name='created_%(class)s_set', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey('users.CustomUser', related_name='updated_%(class)s_set', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-created_at"]
        abstract = True

    def __str__(self):
        return str(self.uuid)

# Custom User model
class CustomUser(AbstractUser, CommonModels):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']  

    objects = CustomUserManager()  # Use the custom manager
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.full_name or self.username or "Unnamed User"
