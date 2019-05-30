from time import ctime


from libs.snowboy.snowboydecoder import play_audio_file, DETECT_DONG
from src.two_relay.actions.actions import find, play, open_action as _open
from src.two_relay.actions.base import launch_application, perform_keyboard_action
from src.deprecated_demos.listen import listen
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
    log("find")
    find(listen("What would you like to find?"))


def music_action():
    log("music")
    play(listen("What song would you like to listen to?"))


def open_action():
    log("open")
    _open(listen("Which file would you like to open?"))


def time_action():
    log("time")
    print(ctime())
