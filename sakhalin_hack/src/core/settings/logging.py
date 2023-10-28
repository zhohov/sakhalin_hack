import os

LOG_LEVEL = os.getenv('LOG_LEVEL')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            "level": LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            "level": LOG_LEVEL,
            'class': "logging.handlers.TimedRotatingFileHandler",
            'filename': "logs/django/debug.log",
            'when': 'midnight',
            'interval': 1,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'level': LOG_LEVEL,
            'handlers': ['console', "file"],
            'propagate': True,
        },
    },
}
