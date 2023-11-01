from django.urls import path
from . import views


app_name = "tasks"
urlpatterns = [
    path('get_tasks/', views.get_tasks, name='GetTasks'),
    path('task_report/<int:task_id>/', views.cleaner_task_report, name='task_report'),
    path('get_cleaner_tasks/<int:cleaner_id>/', views.get_cleaner_tasks, name='get_cleaner_tasks'),
    path('add_task/<int:cleaner_id>/', views.add_task, name='add_task'),
    path('view_report/<int:task_id>', views.view_report, name='view_report')

]
