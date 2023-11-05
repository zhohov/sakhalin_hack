AUTHENTICATION_BACKENDS = (
    'apps.users.auth_backend.PasswordlessAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)
