from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.models import Membership
from .models import Project, ProjectMember
from .serializers import ProjectSerializer, ProjectMemberSerializer

class ProjectCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        org=request.organization
        projects=Project.objects.filter(organization=org)
        serializer=ProjectSerializer(projects,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a project for the current organization.
        Organization is resolved via middleware (request.organization).
        """
        org = request.organization
        if not org:
            return Response(
                {"error": "Organization not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 1. Check membership
        membership = Membership.objects.filter(
            user=request.user, organization=org
        ).first()
        if not membership:
            return Response(
                {"error": "You are not a member of this organization"},
                status=status.HTTP_403_FORBIDDEN
            )

        # 2. Only admins and managers can create
        if membership.role not in ["admin", "manager"]:
            return Response(
                {"error": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Serialize and save
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(organization=org)
            return Response(
                ProjectSerializer(project).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProjectMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organization=request.organization)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)