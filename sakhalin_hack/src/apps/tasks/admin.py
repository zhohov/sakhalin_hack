from django.contrib import admin
from .models import Address, Task, CompletedTask


class TaskAdmin(admin.ModelAdmin):
    ...


class CompletedTaskAdmin(admin.ModelAdmin):
    ...


admin.site.register(Address)
admin.site.register(Task, TaskAdmin)
admin.site.register(CompletedTask, CompletedTaskAdmin)
