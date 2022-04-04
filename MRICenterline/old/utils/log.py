from datetime import datetime, timezone
log_timestamp = datetime.now(timezone.utc).astimezone().isoformat().replace(":", "_")


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'terminal': {
            'format': f'[%(levelname)s] | %(asctime)s | FILE: %(pathname)s | FUNC: %(funcName)s | LINE: %(lineno)d | %(message)s'
        },
        'gui_logger': {
            'format': '[%(levelname)s] | %(asctime)s | %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'terminal',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'terminal',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "./logs/{}.log".format(log_timestamp),
            'maxBytes': 10485760,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
