AUTHENTICATION_BACKENDS = (
    'apps.users.backends.auth_backend.PasswordlessAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)
