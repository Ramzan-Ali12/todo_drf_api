from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100, db_index=True) 
    date = models.DateTimeField(auto_now_add=True) 
    complete = models.BooleanField(default=False, db_index=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')  
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']  
        indexes = [
            models.Index(fields=['user', 'complete']), 
        ]
        verbose_name = 'To-Do'
        verbose_name_plural = 'To-Dos'

    def __str__(self):
        return self.title
