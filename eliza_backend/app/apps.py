from django.apps import AppConfig as Config

initialised = False


class AppConfig(Config):
    name = 'app'

    def ready(self):
        print("ready")
        global initialised
        if not initialised:
            from src.two_relay.get_command import init_recognizer
            init_recognizer()
            from app.views import set_keyword_thread
            from src.main import listen_for_wake_up_word_async
            # set_keyword_thread(listen_for_wake_up_word_async())
            # initialised = True
