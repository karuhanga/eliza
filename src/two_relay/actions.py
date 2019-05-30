import subprocess
import threading
import time

import keyboard

from src.utils.constants import get_music_path, ACTIONS
from src.utils.utils import find_file, get_home_path


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


def launch_application(application, extra_args=None):
    if not application:
        return

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
