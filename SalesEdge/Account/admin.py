from django.contrib import admin

# Register your models here.
from .models import UserProfile, Lead

admin.site.register(UserProfile)
admin.site.register(Lead)