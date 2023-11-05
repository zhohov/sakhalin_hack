from django.contrib import admin
from .models import Appeal, AppealAnswer


class AppealAdmin(admin.ModelAdmin):
    ...


class AppealAnswerAdmin(admin.ModelAdmin):
    ...


admin.site.register(Appeal, AppealAdmin)
admin.site.register(AppealAnswer, AppealAnswerAdmin)
