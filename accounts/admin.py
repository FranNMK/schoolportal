from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the custom User model.
    """
    list_display = ('username', 'email', 'role', 'is_verified', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Attributes', {'fields': ('role', 'phone', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Attributes', {'fields': ('role', 'phone', 'is_verified')}),
    )
