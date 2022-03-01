# DJANGO TELEGRAM LOGGING

This APP was developed on django to provide a simple way of sending error reports of django server via telegram bot API

## Table of Contents
* [instalation](#instalation)
* [configuration](#configuration)


# Instalation: <a name="instalation"></a>
To instalate the appp just execute
```shell
# this command will install the app
$ pip install django-telegram-logging
```

# Configuration: <a name="configuration"></a>
Add django_telegram_logging to your installed apps.
```py
INSTALLED_APPS = [
    ...
    'django_telegram_logging'
]
```
Add to your settings.py file the following variables needed. Is important to add this varaibles to your settings.py file 
before your logging settings.
To get your personal token from Telegram read their [documentation](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
By default TELEGRAM_LOGGING_EMIT_ON_DEBUG is set to false, but if you are running your project on DEBUG mode which you 
shouldn't, you can set this variable to True to emit the log.
```py
TELEGRAM_LOGGING_TOKEN = 'XXXXXXX:XXXXXXXXXXXXXXXXX'
TELEGRAM_LOGGING_CHAT = 12345678
TELEGRAM_LOGGING_EMIT_ON_DEBUG = True
```
Follow [django's documentation](https://docs.djangoproject.com/en/4.0/topics/logging/) to configure logging, add the 
telegram handler to the handlers configuration, and add at least one logger which will use that handler.
```py 
LOGGING = {
    ...
    'handlers': {
        ...
        'telegram': {
            'level': 'ERROR',
            'class': 'django_telegram_logging.handler.TelegramHandler'
        },
    },
    'loggers': {
        ...
        'django': {
            'level': 'ERROR', 
            'handlers': ['console', 'mail_admins', 'telegram']
        }
    }
}
```