from django.contrib.auth.models import AbstractUser
from django.db import models
from django_tenants.models import DomainMixin, TenantMixin
# Create your models here.

class School(TenantMixin):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Domain(DomainMixin):
    pass

class TenantUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.username