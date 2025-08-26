from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.conf import settings


from .models import Organization, Membership, User
from .serializers import InviteMemberSerializer
from core.models import Organization
from .models import Membership
from .serializers import (
    UserSerializer,
    InviteMemberSerializer,
    SignupSerializer,
    OrganizationSerializer,
)
from worker.tasks import send_invite_email

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
        # 1. Check org exists
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found"}, status=404)

        # 2. Only admin can invite
        if not Membership.objects.filter(user=request.user, organization=org, role="admin").exists():
            return Response({"error": "Not allowed"}, status=403)

        # 3. Validate request body
        serializer = InviteMemberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"]
        role = serializer.validated_data["role"]

        # 4. Create/get user
        user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email},
        )

        if created:
            # Temporary password (never sent to user)
            temp_password = get_random_string(10)
            user.set_password(temp_password)
            user.save()

        # 5. Generate token + uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Example: if frontend reset page is at /reset-password/
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        # 6. Send email
        send_invite_email.delay(email, reset_url, org.name) 

        # 7. Add membership
        Membership.objects.get_or_create(user=user, organization=org, role=role)

        return Response(
            {"message": f"{email} invited as {role} to {org.name}"},
            status=status.HTTP_201_CREATED
        )

class ResetPasswordConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        new_password = request.data.get("new_password")
        if not new_password:
            return Response({"error": "Password required"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been set successfully"})
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
