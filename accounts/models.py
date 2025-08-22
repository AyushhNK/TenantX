from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import Organization

class User(AbstractUser):
    # extend if needed (e.g., current_org)
    pass

class Membership(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("employee", "Employee"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organization")