# school/models.py
from django.db import models
from public_app.models import TenantUser


class UserRole(models.Model):
    """Role model to track user roles within a tenant"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]

    user = models.OneToOneField(TenantUser, on_delete=models.CASCADE, related_name='role')
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_admin(self):
        return self.role_type == 'admin'

    @property
    def is_teacher(self):
        return self.role_type == 'teacher'

    @property
    def is_student(self):
        return self.role_type == 'student'

    @property
    def is_parent(self):
        return self.role_type == 'parent'

    def __str__(self):
        return f"{self.user.username} - {self.get_role_type_display()}"


class AdminProfile(models.Model):
    user = models.OneToOneField(TenantUser, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.role}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically create/update role when profile is created
        UserRole.objects.update_or_create(
            user=self.user,
            defaults={'role_type': 'admin'}
        )


class TeacherProfile(models.Model):
    user = models.OneToOneField(TenantUser, on_delete=models.CASCADE, related_name='teacher_profile')
    subject_taught = models.JSONField(default=list)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically create/update role when profile is created
        UserRole.objects.update_or_create(
            user=self.user,
            defaults={'role_type': 'teacher'}
        )


class StudentProfile(models.Model):
    user = models.OneToOneField(TenantUser, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    parent_name = models.CharField(max_length=100)
    parent_contact = models.CharField(max_length=20)
    parent_email = models.CharField(max_length=100)
    address = models.TextField()
    class_level = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='student_profiles/', blank=True)

    def __str__(self):
        return f"{self.user.username} {self.user.role}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically create/update role when profile is created
        UserRole.objects.update_or_create(
            user=self.user,
            defaults={'role_type': 'student'}
        )

    def __str__(self):
        return f"{self.user.username} {self.user.role}"


class ParentProfile(models.Model):
    user = models.OneToOneField(TenantUser, on_delete=models.CASCADE, related_name='parent_profile')
    children = models.ManyToManyField(StudentProfile, related_name='parents')
    occupation = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically create/update role when profile is created
        UserRole.objects.update_or_create(
            user=self.user,
            defaults={'role_type': 'parent'}
        )

    def __str__(self):
        return f"{self.user.username} {self.user.role}"