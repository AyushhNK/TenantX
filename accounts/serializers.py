from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Organization
from .models import Membership
from django.utils.text import slugify

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
        read_only_fields = ["id"]

class InviteMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=Membership.ROLE_CHOICES)

class SignupSerializer(serializers.Serializer):
    org_name = serializers.CharField(max_length=150)
    org_slug = serializers.SlugField(required=False)  # optional, can auto-generate
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_org_slug(self, value):
        if Organization.objects.filter(slug=value).exists():
            raise serializers.ValidationError("This organization slug is already taken.")
        return value

    def create(self, validated_data):
        # Auto-generate slug if not provided
        slug = validated_data.get("org_slug") or slugify(validated_data["org_name"])
        # Ensure uniqueness
        original_slug = slug
        counter = 1
        while Organization.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        # Create organization
        org = Organization.objects.create(
            name=validated_data["org_name"],
            slug=slug
        )

        # Create user
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        # Create membership (admin)
        Membership.objects.create(user=user, organization=org, role="admin")

        return user, org  # return both user and org
    
    class OrganizationMemberSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)
        class Meta:
            model = Membership
            fields = ['id', 'user', 'organization', 'role', 'joined_at']
            read_only_fields = ['id', 'joined_at']