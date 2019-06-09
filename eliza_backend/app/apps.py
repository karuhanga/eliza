from django.apps import AppConfig as Config


class AppConfig(Config):
    name = 'app'

    def ready(self):
        from src.two_relay.get_command import init_recognizer
        init_recognizer()
