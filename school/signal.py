# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import StudentProfile, ParentProfile, UserRole


@receiver(post_save, sender=StudentProfile)
def handle_student_creation(sender, instance, created, **kwargs):
    if created:
        TenantUser = get_user_model()

        # Generate username from parent email
        username_base = instance.parent_email.split('@')[0]
        username = f"parent_{username_base[:15]}"  # Limit username length

        # Create or get parent user
        parent_user, user_created = TenantUser.objects.get_or_create(
            email=instance.parent_email,
            defaults={
                'username': username,
                'password': f"Parent{instance.admission_number}!",  # Temporary password
                'school': instance.user.school,
                'first_name': instance.parent_name.split()[0],
                'last_name': ' '.join(instance.parent_name.split()[1:]) if ' ' in instance.parent_name else '',
            }
        )

        # Create or update parent profile
        parent_profile, _ = ParentProfile.objects.get_or_create(
            user=parent_user,
            defaults={'occupation': ''}
        )
        parent_profile.children.add(instance)

        # Update UserRole if needed
        if user_created:
            UserRole.objects.create(
                user=parent_user,
                role_type='parent'
            )