from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
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


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser where the email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, full_name=None, password=None, **extra_fields):
        if not email or "@" not in email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, password, **extra_fields)
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
