from rest_framework import serializers
from .models import Todo, User


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'completed']


class UserSeriralizer(serializers.ModelSerializer):
    todo_set = TodoSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'todo_set', 'age']