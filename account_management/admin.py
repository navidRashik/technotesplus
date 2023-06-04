from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserAccount


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "is_superuser",
        "is_active",
    ]
    list_filter = [
        "id",
        "username",
        "is_superuser",
    ]
    search_fields = [
        "id",
        "username",
        "is_superuser",
    ]


admin.site.register(UserAccount, UserAdmin)
