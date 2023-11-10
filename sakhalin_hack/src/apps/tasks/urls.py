from django.urls import path
from . import views


app_name = "tasks"
urlpatterns = [
    path('task_report/<int:task_id>/', views.cleaner_task_report, name='task_report'),
    path('get_cleaner_tasks/<int:cleaner_id>/', views.get_cleaner_tasks, name='get_cleaner_tasks'),
    path('add_task/<int:cleaner_id>/', views.add_task, name='add_task'),
    path('view_report/<int:task_id>/', views.view_report, name='view_report'),
    path('create_quality_assessment/<int:task_id>/', views.create_quality_assessment, name='create_quality_assessment'),
    path('view_quality_assessment/<int:task_id>/', views.view_quality_assessment, name='view_quality_assessment'),
    path('get_address_info/<int:address_id>/', views.get_address_info, name='get_address_info'),
    path('get_all_cleaner_tasks/<int:cleaner_id>', views.get_all_cleaner_tasks, name='get_all_cleaner_tasks'),
    path('get_general_report/', views.get_general_report, name='get_general_report')

]
