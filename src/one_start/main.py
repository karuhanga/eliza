import os

from app.socket import socket
from src.one_start.actions.speech import resolve_keyword_action, launch_action, \
    search_action, find_action, music_action, open_action, time_action, \
    what_can_you_do_action
from src.one_start.snowboy import HotWordDetector
from src.utils.constants import ACTIONS


def build_path(param):
    # todo we can do something fancy here like first check for a .pmdl
    #   before falling back to a .umdl
    # return os.path.abspath("src/one_start/data/" + param + ".umdl")
    return "/Users/karuhanga/Projects/FYProject/Elizet/src/one_start/data/" + param + ".umdl"


def build_quick_action_routines(actions):
    return [
        build_routine(action, socket(action))
        for action in actions
    ]


def build_routine(name, callback, sensitivity=0.4):
    return {
            "name": name,
            "model": build_path(name),
            "callback": callback,
            "sensitivity": sensitivity
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
    # launch
    routines.append(build_routine("launch", socket("launch")))
    routines.append(build_routine("launch_app", launch_action))
    # search
    routines.append(build_routine("search", socket("search")))
    # find
    routines.append(build_routine("find", socket("find")))
    # music
    routines.append(build_routine("music", socket("music")))
    # open
    routines.append(build_routine("open", socket("open")))
    routines.append(build_routine("open_file", open_action))
    # time
    routines.append(build_routine("time", socket("time")))
    # what_can_you_do_action
    # routines.append(build_routine("what_can_you_do_action", what_can_you_do_action))
    # quick action routines
    routines.extend(build_quick_action_routines(ACTIONS.keys()))

    return HotWordDetector(routines)
