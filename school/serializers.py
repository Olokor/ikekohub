from rest_framework import serializers

from public_app.models import School
from school.models import TenantUser, TeacherProfile, StudentProfile


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'school']

class AdminProfileSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    class Meta:
        model = TenantUser
        fields = '__all__'


class TeacherProfileCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    school = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = TeacherProfile
        fields = [
            'username', 'email', 'password', 'school',
             # Add other teacher profile fields
        ]

    def validate(self, data):
        # Check if school exists
        if not School.objects.filter(name=data['school']).exists():
            raise serializers.ValidationError({
                'school': f"School '{data['school']}' does not exist."
            })
        return data

    def create(self, validated_data):
        # Extract user creation data
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'password': validated_data['password'],
            'school': School.objects.get(name=validated_data['school'])
        }

        # Create user
        user = TenantUser.objects.create_user(**user_data)

        # Create teacher profile
        teacher_profile = TeacherProfile.objects.create(
            user=user
        )
        return {
            'id': teacher_profile.id,
            'username': user.username,
            'email': user.email,
            'school': validated_data['school']
        }


class StudentProfileCreateSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)
    username = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    school = serializers.CharField(write_only=True, required=True)
    parent_email = serializers.EmailField(required=True)
    parent_name = serializers.CharField(required=True, max_length=100)
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'username', 'email', 'password', 'school',
            'admission_number', 'date_of_birth', 'parent_name',
            'parent_email', 'address', 'parent_contact',
            'class_level', 'academic_year'
        ]
        read_only_fields = ['id', 'user']

    def validate(self, data):
        if not School.objects.filter(name=data['school']).exists():
            raise serializers.ValidationError({
                'school': f"School '{data['school']}' does not exist."
            })
        return data

    def create(self, validated_data):
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'password': validated_data['password'],
            'school': School.objects.get(name=validated_data['school'])
        }

        user = TenantUser.objects.create_user(**user_data)
        student_profile = StudentProfile.objects.create(
            user=user,
            admission_number=validated_data['admission_number'],
            date_of_birth=validated_data['date_of_birth'],
            parent_name=validated_data['parent_name'],
            parent_email=validated_data['parent_email'],
            address=validated_data['address'],
            parent_contact=validated_data['parent_contact'],
            class_level=validated_data['class_level'],
            academic_year=validated_data['academic_year'],
        )

        return {
            'id': student_profile.id,
            'username': user.username,
            'email': user.email,
            'school': validated_data['school'],
            'admission_number': validated_data['admission_number'],
            'date_of_birth': validated_data['date_of_birth'],
            'parent_name': validated_data['parent_name'],
            'parent_email': validated_data['parent_email'],
            'address': validated_data['address'],
            'parent_contact': validated_data['parent_contact'],
            'class_level': validated_data['class_level'],
            'academic_year': validated_data['academic_year'],
            'parent_username': student_profile.parents.first().user.username if student_profile.parents.exists() else None
        }
