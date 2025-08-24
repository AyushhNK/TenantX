from django.contrib import admin
from .models import User, Membership

# Register your models here.
admin.site.register(User)
admin.site.register(Membership)