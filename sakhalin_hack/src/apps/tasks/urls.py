from django.urls import path
from . import views


app_name = "tasks"
urlpatterns = [
    path('get_tasks/', views.get_tasks, name='GetTasks'),
    path('task_report/<int:task_id>/', views.cleaner_task_report, name='task_report'),
]
