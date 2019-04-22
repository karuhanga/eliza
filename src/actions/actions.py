import subprocess
import threading
import time

import keyboard

from src.actions.base import windows_action
from src.utils.constants import get_music_path
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
