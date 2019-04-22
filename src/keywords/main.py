import os

from src.keywords.actions import resolve_keyword_action, launch_action, \
    search_action, find_action, play_action, open_action, sleep_action, \
    select_all_action
from src.keywords.snowboy import HotWordDetector
from src.utils.constants import ACTIONS


def build_path(param):
    # todo we can do something fancy here like first check for a .pmdl
    #   before falling back to a .umdl
    return os.path.abspath("src/keywords/data/" + param + ".umdl")


def build_quick_action_routines(actions):
    return [
        build_routine(action, resolve_keyword_action(action))
        for action in actions
    ]


def build_routine(name, callback):
    return {
            "name": name,
            "model": build_path(name),
            "callback": callback
        }


def build_wake_up_detector(trigger, action):
    routines = []
    # test routine
    routines.append(build_routine(trigger, action))
    return HotWordDetector(routines)


def build_detector(stop_trigger, stop_action):
    routines = []
    # stop routine
    routines.append(build_routine(stop_trigger, stop_action))
    # quick action routines
    routines.extend(build_quick_action_routines(ACTIONS.keys()))
    # open
    routines.append(build_routine("launch", launch_action))
    # search
    routines.append(build_routine("search", search_action))
    # find
    routines.append(build_routine("find", find_action))
    # play
    routines.append(build_routine("play", play_action))
    # open
    routines.append(build_routine("open", open_action))
    # sleep
    routines.append(build_routine("sleep", sleep_action))
    # select all
    routines.append(
        build_routine("select_all", select_all_action)
    )

    return HotWordDetector(routines)
