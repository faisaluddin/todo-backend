from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Task


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


class StatsSerializer(serializers.ModelSerializer):
    tasks_completed = serializers.SerializerMethodField()
    total_tasks = serializers.SerializerMethodField()
    latest_tasks = serializers.SerializerMethodField()

    def get_tasks_completed(self, obj):
        return obj.filter(completed=True).count()

    def get_total_tasks(self, obj):
        return obj.all().count()

    def get_latest_tasks(self, obj):
        return [t.name for t in obj.all()[:3]]

    class Meta:
        model = Task
        fields = ('tasks_completed', 'total_tasks', 'latest_tasks', )
