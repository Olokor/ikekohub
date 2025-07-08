from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from public_app.models import TenantUser, School
from .models import StudentProfile, TeacherProfile, AdminProfile, UserRole
from .permissions import (
    IsAdmin, IsTeacher, IsStudent, IsAdminOrTeacher,
    IsOwnerOrAdminOrTeacher, IsStudentOwnerOrParentOrTeacher
)
from .serializers import AdminProfileSerializer, TeacherProfileCreateSerializer


# Admin-only view
class AdminDashboardView(generics.GenericAPIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Welcome to admin dashboard"})


class CreateTeacherView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = TeacherProfileCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        teacher_data = serializer.save()
        return Response(teacher_data, status=status.HTTP_201_CREATED)


class GetAllUsersView(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    # serializer_class =
    def get(self, request, user_role=None):
        # if user_role:
        #     users = get_user_model().objects.filter(role_type=user_role)
        #     return Response({"users": users})
        return Response({"users": get_user_model().objects.all()})
