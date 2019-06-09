import os

from django.apps import AppConfig as Config

from src.two_relay.give_answer import init_wolfi


class AppConfig(Config):
    name = 'app'

    def ready(self):
        print("ready")
        if os.environ.get('RUN_MAIN', None) == 'true':
            from src.two_relay.get_command import init_recognizer
            init_recognizer()
            init_wolfi()
            from app.views import set_keyword_thread, stop_keyword
            from src.main import listen_for_wake_up_word_async
            stop_keyword()
            set_keyword_thread(listen_for_wake_up_word_async())
