from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Company, CustomUser


class CustomUserAdmin(UserAdmin):
    list_filter = [
        'company',
        'groups',
    ]

    list_display = (
        'username',
        'first_name',
        'last_name',
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            None,
            {
                'fields': (
                    'photo',
                    'phone_number',
                    'company'
                ),
            },
        ),
    )


admin.site.register(Company)
admin.site.register(CustomUser, CustomUserAdmin)
