from rest_framework import serializers
from .models import Project,ProjectMember

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "organization", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']       