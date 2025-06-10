from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Roles, Permissions, UserRole
from .forms import UserCreationForm, CustomUserChangeForm

# Inline for assigning roles to a user
class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    inlines = [UserRoleInline]

    list_display = ("email", "first_name", "last_name", "is_verified_by_admin", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_verified_by_admin", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active")}
        ),
    )

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name",)
    list_filter = ("status",)
    filter_horizontal = ("permissions",)  # for better M2M UI

@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("name",)
    ordering = ("code",)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "created_at")
    list_filter = ("user", "role")
    search_fields = ("user__email", "role__name")
