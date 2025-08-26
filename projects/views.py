from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from core.models import Organization
from accounts.models import Membership
from .models import Project
from .serializers import ProjectSerializer

class ProjectCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, org_id):
        # 1. Check if organization exists
        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found"}, status=404)

        # 2. Check if user belongs to this org
        membership = Membership.objects.filter(user=request.user, organization=org).first()
        if not membership:
            return Response({"error": "You are not a member of this organization"}, status=403)

        # 3. Only allow admins and managers to create projects
        if membership.role not in ["admin", "manager"]:
            return Response({"error": "Not allowed"}, status=403)

        # 4. Serialize and save project
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(organization=org)
            return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
