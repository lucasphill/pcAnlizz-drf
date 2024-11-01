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

# class Estudantes(admin.ModelAdmin):
#     list_display = ('id', 'nome', 'email', 'cpf', 'data_nascimento', 'numero_celular',)
#     list_display_links = ('id', 'nome')
#     list_per_page = 20
#     search_fields = ('nome', 'cpf',)
#     ordering = ('nome',)

# admin.site.register(Estudante, Estudantes)

# Register your models here.

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import CustomUser


# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ("email", "is_staff", "is_active",)
#     list_filter = ("email", "is_staff", "is_active",)
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
#     )
#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": (
#                 "email", "password1", "password2", "is_staff",
#                 "is_active", "groups", "user_permissions"
#             )}
#         ),
#     )
#     search_fields = ("email",)
#     ordering = ("email",)


# admin.site.register(CustomUser, CustomUserAdmin)