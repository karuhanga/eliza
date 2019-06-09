from src.one_start.actions.weather import run
from src.utils.constants import ACTIONS, LAUNCHER_COMMANDS, \
    get_launcher_commands

from time import ctime


from src.two_relay.actions import find, play, open_action as _open, \
    perform_keyboard_action, launch_application
from src.utils.utils import log


def resolve_keyword_action(action):
    def to_call():
        log(action)
        perform_keyboard_action(action)
    return to_call


def launch_action(application_name):
    log("launch")
    if application_name not in get_launcher_commands():
        return application_name + " could not be found. Install this application?"
    launch_application(application_name)


def search_action(query):
    log("search")
    launch_application(
        "firefox",
        extra_args=["--search", query]
    )


def find_action(file_name):
    log("find")
    find(file_name)


def music_action(song):
    log("music")
    play(song)


def open_action(file_name):
    log("open")
    _open(file_name)


def time_action():
    log("time")
    return str(ctime())


def what_can_you_do_action():
    log("what can you do?")
    return \
        """
            Hey, I'm Eliza. I can;\n
            - Tell you the time.
            - Open applications
            - Play music
            - Open files
            - Find files and applications
        """


def weather_action(where='Kampala'):
    return run(where=where)


def build_action(name, steps, last_n_prompts, action):
    return {
        'name': name,
        'steps': steps,
        'last_n_prompts': last_n_prompts,
        'action': action,
    }


def build_actions():
    results = {
        'launch': build_action("launch", 2, ["Which application would you like to open?", "Launching "], launch_action),
        'search': build_action("search", 2, ["What would you like me to search for?", "Searching "], search_action),
        'time': build_action("time", 1, [""], time_action),
        'what can you do?': build_action("what can you do?", 1, [""], what_can_you_do_action),
        'weather': build_action('weather', 2, ["Where?", ""], weather_action)
    }
    quick_actions = [{action: build_action(action, 1, ["Done."], resolve_keyword_action(action))} for action in ACTIONS.keys()]
    for action in quick_actions:
        results.update(action)
    return results


actions = build_actions()
