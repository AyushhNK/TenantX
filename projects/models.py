from django.db import models
from core.models import BaseTenantModel

# Create your models here.
class Project(BaseTenantModel):
    name = models.CharField(max_length=255)
