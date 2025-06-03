from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Roles, Permissions, Roles_Permissions, UserRole
from .forms import UserCreationForm, CustomUserChangeForm

class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1

class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    inlines = [UserRoleInline]


    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser")
    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
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


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("name",)
    ordering = ("code",)


@admin.register(Roles_Permissions)
class RolesPermissionsAdmin(admin.ModelAdmin):
    list_display = ("role", "permission")
    list_filter = ("role", "permission")
    search_fields = ("role__name", "permission__name")

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("user", "role")



# Register the custom user model
admin.site.register(CustomUser, CustomUserAdmin)
