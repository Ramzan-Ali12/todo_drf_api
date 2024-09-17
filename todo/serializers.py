from .models import Todo
from rest_framework import serializers

class TodoSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Todo
        fields = 'title', 'date', 'complete', 'user','updated'

