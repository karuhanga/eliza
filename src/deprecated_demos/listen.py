from app.socket import socket
from src.two_relay.get_command import get_command
from src.utils.utils import threaded


def listen(message):
    command = get_command(message=message)
    if command:
        return command
    print("Sorry, I didn't get that")


@threaded
def listen_async():
    from src.one_start.actions.speech import eliza_action
    eliza_action()
    message = listen("blah")
    print("Recognized: " + str(message))
    if not message:
        message = "Sorry, I didn't get that"
        socket(message, True)()
    socket(message)()
    from app.views import set_keyword_thread, stop_keyword
    from src.main import listen_for_wake_up_word_async
    stop_keyword()
    set_keyword_thread(listen_for_wake_up_word_async())


def end_listening_for_generic():
    return None  # todo
