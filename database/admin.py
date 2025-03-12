from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "user_type", "is_staff")
    list_filter = ("user_type", "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "phone", "picture")}),
        (
            "Address",
            {
                "fields": (
                    "street",
                    "street_number",
                    "apartment",
                    "city",
                    "state",
                    "zip_code",
                    "country",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "user_type",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)


admin.site.register(CustomUser, CustomUserAdmin)
