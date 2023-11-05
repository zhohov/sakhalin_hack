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
        (
            'Персональная информация',
            {
                'fields': (
                    'photo',
                    'username',
                    'first_name',
                    'last_name',
                    'middle_name',
                    'email',
                    'password',
                    'phone_number',
                    'company',
                    'phone_code'
                ),
            },
        ),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)})
    )


admin.site.register(Company)
admin.site.register(CustomUser, CustomUserAdmin)
