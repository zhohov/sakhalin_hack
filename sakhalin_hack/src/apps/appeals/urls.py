from django.urls import path
from . import views


app_name = 'appeals'
urlpatterns = [
    path('create_appeal/', views.create_appeal, name='create_appeal'),
    path('create_appeal_answer/<int:appeal_id>/', views.create_appeal_answer, name='create_appeal_answer'),
    path('view_appeal_answer/<int:appeal_id>/', views.view_appeal_answer, name='view_appeal_answer'),

]
