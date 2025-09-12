from django.db import models
from core.models import BaseTenantModel
from accounts.models import User

# Create your models here.
class Project(BaseTenantModel):
    name = models.CharField(max_length=255)


class ProjectMember(BaseTenantModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    role = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ('organization', 'project', 'user')

    def __str__(self):
        return f"{self.user} in {self.project}"