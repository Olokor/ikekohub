# permissions.py
from rest_framework import permissions

from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Permission for admin users within their school"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        try:
            # Check if user is admin
            if not request.user.role.is_admin:
                return False

            # Get school from request data or user
            user_school = request.user.school

            # If creating teacher, ensure they belong to same school
            if hasattr(request.user, 'school') and user_school:
                return True

            return False
        except AttributeError:
            return False
class IsTeacher(permissions.BasePermission):
    """Permission for teacher users only"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.role.is_teacher
        except AttributeError:
            return False


class IsStudent(permissions.BasePermission):
    """Permission for student users only"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.role.is_student
        except AttributeError:
            return False


class IsParent(permissions.BasePermission):
    """Permission for parent users only"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.role.is_parent
        except AttributeError:
            return False


class IsAdminOrTeacher(permissions.BasePermission):
    """Permission for admin or teacher users"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.role.is_admin or request.user.role.is_teacher
        except AttributeError:
            return False


class IsTeacherOrReadOnly(permissions.BasePermission):
    """Allow teachers full access, others read-only"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Allow read access for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow write access only for teachers
        try:
            return request.user.role.is_teacher
        except AttributeError:
            return False


class IsOwnerOrAdminOrTeacher(permissions.BasePermission):
    """Allow access to resource owner, admin, or teacher"""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        try:
            # Allow admin and teacher full access
            if request.user.role.is_admin or request.user.role.is_teacher:
                return True

            # Allow users to access their own objects
            if hasattr(obj, 'user'):
                return obj.user == request.user

            return False
        except AttributeError:
            return False


class IsStudentOwnerOrParentOrTeacher(permissions.BasePermission):
    """Allow student to access their own data, or parent/teacher to access student data"""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        try:
            # Admin and teachers can access all student data
            if request.user.role.is_admin or request.user.role.is_teacher:
                return True

            # Students can access their own profile
            if request.user.role.is_student:
                return obj.user == request.user

            # Parents can access their children's data
            if request.user.role.is_parent:
                # Check if this student is the parent's child
                return obj in request.user.parent_profile.children.all()

            return False
        except AttributeError:
            return False