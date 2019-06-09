import os

from django.apps import AppConfig as Config


class AppConfig(Config):
    name = 'app'

    def ready(self):
        print("ready")
        if os.environ.get('RUN_MAIN', None) == 'true':
            from src.two_relay.get_command import init_recognizer
            init_recognizer()
            from app.views import set_keyword_thread, stop_keyword
            from src.main import listen_for_wake_up_word_async
            stop_keyword()
            set_keyword_thread(listen_for_wake_up_word_async())
