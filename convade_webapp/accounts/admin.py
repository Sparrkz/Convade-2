from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile
from django.db import models

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Profile', {
            'fields': ('role', 'profile_picture', 'bio', 'phone_number', 'date_of_birth')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Profile', {
            'fields': ('role', 'profile_picture', 'bio', 'phone_number', 'date_of_birth')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        # Show all fields in list_display
        self.list_display = ['user'] + [field.name for field in model._meta.fields if field.name not in ('id', 'user')]

        # Search only text-based fields
        self.search_fields = [
            field.name for field in model._meta.fields
            if isinstance(field, (models.CharField, models.TextField))
        ]

        # Filter on all choice or foreign key fields
        self.list_filter = [
            field.name for field in model._meta.fields
            if field.choices or field.get_internal_type() in ["ForeignKey"]
        ]
