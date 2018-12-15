import subprocess
import threading
import time

import keyboard

from utils.constants import SLEEP_ACTION, MUSIC_PATH
from utils.utils import find_file, get_home_path

ACTIONS = {
    # app specific commands todo customise these from context
    "save":         "ctrl+s",
    "close":        "alt+F4",
    "pause":        "space",
    "play": "space",
    # system commands
    "lock":         "win+l",
    "minimise":     "win+down",
    "maximise":     "win+up",
    "undo":         "ctrl+z",
    "cut":          "ctrl+x",
    "copy":         "ctrl+c",
    "paste":        "ctrl+v",
    "desktop":      "win+d",
    "switch":       "win+tab",
    "screenshot":   "prtsc",
    # todo account for other commands
}


def launch_application(application, extra_args=None):
    def runner():
        extras = [] if extra_args is None else extra_args
        if "firefox" in application:
            args = ["su", "karuhanga", "-c", "firefox"]
            args.extend(extras)
            subprocess.call(args)
        elif "chrome" in application or "chromium" in application:
            subprocess.call(["su", "karuhanga", "-c", "chromium-browser"])
        elif "vlc" in application:
            subprocess.call(["su", "karuhanga", "-c", "vlc"])
        elif "sublime" in application:
            subprocess.call(["su", "karuhanga", "-c", "subl"])
        elif "files" in application:
            subprocess.call(["su", "karuhanga", "-c", "nautilus"])

    threading.Thread(target=runner).start()


def perform_complex_action(command):
    if command == "select all":
        run_keyboard_action("ctrl+a")
    else:
        command_list = command.split(" ")
        action = command_list[0]
        command_list = command_list[1:]
        if action == "launch":
            application = " ".join(command_list)
            application = application.strip()
            launch_application(application)
        elif action == "search" or action == "google":
            query = " ".join(command_list)
            query = query.strip()
            launch_application("firefox", extras=["--search", query])
            perform_action("switch")
        elif action == "find":
            query = " ".join(command_list)
            query = query.strip()
            windows_action()
            time.sleep(1)
            keyboard.write(query)
        elif action == "elisa" or action == "eliza":  # todo find universal way of accounting for such errors
            cmd = " ".join(command_list)
            cmd = cmd.strip()
            if cmd == "sleep":
                run_keyboard_action(SLEEP_ACTION)
        elif action == "play":
            def runner():
                track = " ".join(command_list)
                track = track.strip()
                options = find_file(track, MUSIC_PATH, "mp3")
                if len(options):
                    subprocess.call(["xdg-open", options[0]])
                else:
                    options = find_file('*' + track + '*', MUSIC_PATH, "mp3")
                    if len(options):
                        subprocess.call(["xdg-open", options[0]])

            threading.Thread(target=runner).start()
        elif action == "open":  # todo make this a persistence based search(too slow)
            file = " ".join(command_list)
            file = file.strip()
            options = find_file(file, get_home_path(), "*")
            print(options)
            if len(options):
                subprocess.call(["xdg-open", options[0]])
            else:
                options = find_file('*' + file + '*', get_home_path(), "*")
                if len(options):
                    subprocess.call(["xdg-open", options[0]])
        else:
            perform_complex_action("search " + command)
    # todo add other actions


def run_keyboard_action(action):
    if action:
        if "win+" in action:
            action = action.replace("win+", "")
            windows_action(action)
        elif "prtsc" in action:
            keyboard.send(99)
        else:
            keyboard.send(action)


def perform_action(command):
    if " " in command:
        return perform_complex_action(command)
    run_keyboard_action(resolve_simple_action(command))


def windows_action(combo=None):
    if combo:
        keyboard.send(125, do_press=True, do_release=False)
        keyboard.send(combo, do_press=True, do_release=False)
        keyboard.send(125, do_press=False, do_release=True)
        keyboard.send(combo, do_press=False, do_release=True)
    else:
        keyboard.send(125)


def resolve_simple_action(command):
    try:
        return ACTIONS[command]
    except KeyError:
        print("No action for {} command".format(command))
        perform_complex_action("search " + command)
        return
