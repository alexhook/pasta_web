from django.contrib import admin
from .models import UserPersonalInfo

@admin.register(UserPersonalInfo)
class UserPersonalInfoAdmin(admin.ModelAdmin):
    pass
