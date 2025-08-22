from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Organization
from .models import Membership

User = get_user_model()

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "slug", "created_at"]
        read_only_fields = ["id", "created_at"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class InviteMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=Membership.ROLE_CHOICES)

class SignupSerializer(serializers.Serializer):
    org_name = serializers.CharField(max_length=150)
    org_slug = serializers.SlugField()
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        org = Organization.objects.create(name=validated['org_name'], slug=validated['org_slug'])
        user = User.objects.create_user(
            username=validated['username'], email=validated['email'], password=validated['password']
        )
        Membership.objects.create(user=user, organization=org, role='admin')