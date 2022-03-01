import logging
import requests
from copy import copy
from datetime import datetime
from django.conf import settings
from django.utils.module_loading import import_string


token = settings.TELEGRAM_LOGGING_TOKEN
chat = settings.TELEGRAM_LOGGING_CHAT
emit_on_debug = getattr(settings, 'TELEGRAM_LOGGING_EMIT_ON_DEBUG', False)


class PseudoFile:
    def __init__(self, content, name):
        self.name = name
        self.content = content

    def read(self):
        return self.content


class TelegramHandler(logging.Handler):
    # noinspection PyUnusedLocal
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.include_html = True
        self.reporter_class = import_string('django.views.debug.ExceptionReporter')

    def emit(self, record):
        if settings.DEBUG and not emit_on_debug:
            return
        # noinspection PyBroadException
        try:
            # noinspection PyUnresolvedReferences
            request = record.request
        except Exception:
            request = None

        # Since we add a nicely formatted traceback on our own, create a copy
        # of the log record without the exception data.
        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = self.reporter_class(request, *exc_info)
        html_message = reporter.get_traceback_html()
        self.send_message(html_message)

    def send_message(self, html_message):
        try:
            document_name = f'{datetime.now().strftime("%Y%m%d%H%M%S")}.{logging.getLevelName(self.level)}.html'
            requests.post(
                f'https://api.telegram.org/bot{token}/sendDocument',
                data={'chat_id': chat},
                files={'document': PseudoFile(html_message, document_name)}
            )
        except Exception as e:
            print(f'we got an error when handling the exception => {e}')
