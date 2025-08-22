from django.db import models
from django.conf import settings

class Organization(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class BaseTenantModel(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="%(class)s_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True