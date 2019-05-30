import keyboard

from src.two_relay.actions.base import perform_keyboard_action
from src.two_relay import get_command
from src.utils.constants import COMMAND_SCOPE

in_the_middle_of_something = False


def runner():
    global in_the_middle_of_something
    if in_the_middle_of_something:
        return
    in_the_middle_of_something = True
    command = get_command(command_scope=COMMAND_SCOPE)
    if command:
        print("Running action: {}".format(command))
        perform_keyboard_action(command)
    in_the_middle_of_something = False


if __name__ == "__main__":
    print("Started")
    keyboard.add_hotkey('`', runner)
    keyboard.wait('ctrl+esc')
