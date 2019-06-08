import subprocess
import threading
import time

import delegator
import keyboard

from src.utils.constants import get_music_path, ACTIONS, get_launcher_command_action
from src.utils.utils import find_file, get_home_path, threaded


def find(query):
    query = query.strip()
    windows_action()
    time.sleep(1)
    keyboard.write(query)


def play(track):
    def runner(track):
        track = track.strip()
        options = find_file(track, get_music_path(), "mp3")
        if len(options):
            subprocess.call(["xdg-open", options[0]])
        else:
            options = find_file('*' + track + '*', get_music_path, "mp3")
            if len(options):
                subprocess.call(["xdg-open", options[0]])

    threading.Thread(target=lambda: runner(track)).start()


def open_action(file):
    def runner(file):
        file = file.strip()
        options = find_file(file, get_home_path(), "*")
        print(options)
        if len(options):
            subprocess.call(["xdg-open", options[0]])
        else:
            options = find_file('*' + file + '*', get_home_path(), "*")
            if len(options):
                subprocess.call(["xdg-open", options[0]])

    threading.Thread(target=lambda: runner(file)).start()


@threaded
def launch_application(application, extra_args=None):
    if not application:
        return

    print("Launching " + application)

    extras = [] if extra_args is None else extra_args

    try:
        command_list = [get_launcher_command_action(application)]
        command_list.extend(extras)
        delegator.run(command_list)
    except KeyError:
        return False

    return True


def run_keyboard_action(action):
    if action:
        if "win+" in action:
            action = action.replace("win+", "")
            windows_action(action)
        elif "prtsc" in action:
            keyboard.send(99)
        else:
            keyboard.send(action)


def perform_keyboard_action(command):
    run_keyboard_action(ACTIONS[command])


def windows_action(combo=None):
    if combo:
        keyboard.send(125, do_press=True, do_release=False)
        keyboard.send(combo, do_press=True, do_release=False)
        keyboard.send(125, do_press=False, do_release=True)
        keyboard.send(combo, do_press=False, do_release=True)
    else:
        keyboard.send(125)
