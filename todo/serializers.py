from .models import Todo
from rest_framework import serializers

class TodoSerializer(serializers.ModelSerializer):
    # The user field can be read-only since the logged-in user will be associated with the todo

    class Meta:
        model = Todo
        fields = ['uuid', 'title', 'description', 'completed','created_at', 'updated_at']
    
    
