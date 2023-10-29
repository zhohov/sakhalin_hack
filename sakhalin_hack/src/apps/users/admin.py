from django.contrib import admin

from .models import Company, CustomUser, Clearing


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = [
        'company',
        'groups',
    ]

    list_display = (
        'first_name',
        'last_name',
    )


class ClearingAdmin(admin.ModelAdmin):
    list_filter = [
        'cleaner',
    ]


admin.site.register(Company)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Clearing, ClearingAdmin)
