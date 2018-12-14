import time

import keyboard
import subprocess


def launch_application(application, extras=None):
    extras = [] if extras is None else extras
    if "firefox" in application:
        args = ["sudo", "-u", "karuhanga", "firefox"]
        args.extend(extras)
        subprocess.call(args)
    elif "chrome" in application or "chromium" in application:
        subprocess.call(["sudo", "-u", "karuhanga", "chromium-browser"])
    elif "vlc" in application:
        subprocess.call(["sudo", "-u", "karuhanga", "vlc"])
    elif "sublime" in application:
        subprocess.call(["sudo", "-u", "karuhanga", "subl"])
    elif "files" in application:
        subprocess.call(["sudo", "-u", "karuhanga", "nautilus"])


def perform_complex_action(command):
    if command == "select all":
        run_keyboard_action("ctrl+a")
    else:
        command_list = command.split(" ")
        action = command_list[0]
        command_list = command_list[1:]
        if action == "open":
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
    # todo add other actions


def run_keyboard_action(action):
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
    if command == "save":
        return "ctrl+s"
    elif command == "close":
        return "alt+F4"
    elif command == "pause":
        return "space"
    elif command == "lock":
        return "win+l"
    elif command == "minimise":
        return "win+down"
    elif command == "maximise":
        return "win+up"
    elif command == "undo":
        return "ctrl+z"
    elif command == "cut":
        return "ctrl+x"
    elif command == "copy":
        return "ctrl+c"
    elif command == "paste":
        return "ctrl+v"
    elif command == "desktop":
        return "ctrl+d"
    elif command == "switch":
        return "win+tab"
    elif command == "screenshot":
        return "prtsc"

    # todo account for other commands
