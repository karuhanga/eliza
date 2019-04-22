from src.actions.actions import find, play, open_action as _open, sleep, \
    select_all
from src.actions.base import launch_application, perform_keyboard_action
from src.relays.listen import listen


def snow_boy_action():
    print("Snowboy!")


def resolve_keyword_action(action):
    return lambda: perform_keyboard_action(action)


def launch_action():
    status = launch_application(listen("Which application would you like to open?"))
    if status:
        perform_keyboard_action("switch")


def search_action():
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
