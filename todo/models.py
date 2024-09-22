from django.db import models
from users.models import CustomUser, CommonModels

class Todo(CommonModels):
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    completed = models.BooleanField(db_index=True, default=False)
    user = models.ForeignKey(CustomUser, related_name="todos", on_delete=models.CASCADE)  # Add the ForeignKey to CustomUser


    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.title
    