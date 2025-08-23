from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

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

            user, _ = User.objects.get_or_create(
                username=email,
                defaults={"email": email},
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
