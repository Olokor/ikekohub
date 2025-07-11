from django.contrib import admin

from school.models import AdminProfile, StudentProfile, TeacherProfile
from school.serializers import AdminProfileSerializer

# Register your models here.
admin.site.register(AdminProfile)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)