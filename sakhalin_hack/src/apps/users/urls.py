from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.user_profile, name='user_profile'),
    path('email_login/', views.email_login, name='email_login'),
    path('phone_number_login/', views.phone_number_login, name='phone_number_login'),
    path('otp_verified/<int:user_id>/', views.otp_verified, name='otp_verified')

]
