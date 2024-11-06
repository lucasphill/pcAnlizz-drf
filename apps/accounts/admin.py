from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import User

class Users(admin.ModelAdmin):
    # list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined', 'groups', 'user_permissions')
    list_display = ('username', 'email', 'first_name', 'is_superuser', 'last_login', 'date_joined', 'is_active',)
    list_display_links = ('username',)
    list_per_page = 20
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(User, Users)