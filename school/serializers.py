from rest_framework import serializers

from public_app.models import School
from school.models import TenantUser, TeacherProfile


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

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
                'school': f"School '{data['school']}' does not exist. Available schools: {list(School.objects.values_list('name', flat=True))}"
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
        print( {
            'id': teacher_profile.id,
            'username': user.username,
            'email': user.email,
            'school': validated_data['school']
        })
        return {
            'id': teacher_profile.id,
            'username': user.username,
            'email': user.email,
            'school': validated_data['school']
        }

