from libs.snowboy.snowboydecoder import play_audio_file, DETECT_DONG
from src.actions.actions import find, play, open_action as _open, sleep, \
    select_all
from src.actions.base import launch_application, perform_keyboard_action
from src.relays.listen import listen
from src.utils.utils import log


def eliza_action():
    play_audio_file(DETECT_DONG)
    print("Hey!")


def resolve_keyword_action(action):
    def to_call():
        log(action)
        perform_keyboard_action(action)
    return to_call


def launch_action():
    log("launch")
    status = launch_application(listen("Which application would you like to open?"))
    if status:
        perform_keyboard_action("switch")


def search_action():
    log("search")
    launch_application(
        "firefox",
        extra_args=["--search", listen("What would you like to search for?")]
    )
    perform_keyboard_action("switch")


def find_action():
    find(listen("What would you like to find?"))


def play_action():
    play(listen("What song would you like to listen to?"))


def open_action():
    _open(listen("Which file would you like to open?"))


def sleep_action():
    sleep()


def select_all_action():
    select_all()
