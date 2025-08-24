from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse

from core.models import Organization
from .models import Membership
from .serializers import (
    UserSerializer,
    InviteMemberSerializer,
    SignupSerializer,
    OrganizationSerializer,
)

User = get_user_model()


# ---------------------------
# Get Current User Profile
# ---------------------------
class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# ---------------------------
# Signup (User + Org + Admin Membership)
# ---------------------------
class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user, org = serializer.save()  # returns both user and org

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                "user": UserSerializer(user).data,
                "organization": OrganizationSerializer(org).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# Login (JWT)
# ---------------------------
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# ---------------------------
# Invite Member to Organization
# ---------------------------
class InviteMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, org_id):
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found"}, status=404)

        # only admin can invite
        if not Membership.objects.filter(user=request.user, organization=org, role="admin").exists():
            return Response({"error": "Not allowed"}, status=403)

        serializer = InviteMemberSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            role = serializer.validated_data["role"]

            user,created = User.objects.get_or_create(
                username=email,
                defaults={"email": email},
            )
            if created:
                # Generate temporary password (not shared with user)
                temp_password = "Testing123."
                user.set_password(temp_password)
                user.save()

                # Generate password reset link
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(
                    reverse("password_reset_confirm", args=[user.pk, token])
                )

                # Send email with reset link
                send_mail(
                    "You're invited to TenantX",
                    f"Hello, please set your password here: {reset_url}",
                    "noreply@tenantx.com",
                    [email],
                )

            Membership.objects.get_or_create(user=user, organization=org, role=role)

            return Response({
                "message": f"{email} invited as {role} to {org.name}"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# My Memberships
# ---------------------------
class MyMembershipsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        memberships = Membership.objects.filter(user=request.user).select_related("organization")
        data = [
            {
                "organization": OrganizationSerializer(m.organization).data,
                "role": m.role,
                "joined_at": m.joined_at,
            }
            for m in memberships
        ]
        return Response(data)


# ---------------------------
# Switch Organization
# ---------------------------
class SwitchOrganizationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        org_id = request.data.get("org_id")
        if not Membership.objects.filter(user=request.user, organization_id=org_id).exists():
            return Response({"error": "Not part of this organization"}, status=403)

        request.session["current_org_id"] = org_id
        return Response({"message": "Organization switched"})
