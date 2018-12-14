import keyboard

from demos.action_resolver import perform_action
from demos.get_command import get_command
from utils.constants import COMMAND_SCOPE

in_the_middle_of_something = False


def runner():
    global in_the_middle_of_something
    if in_the_middle_of_something:
        return
    in_the_middle_of_something = True
    command = get_command(command_scope=COMMAND_SCOPE)
    if command:
        print("Running action: {}".format(command))
        perform_action(command)
    in_the_middle_of_something = False


if __name__ == "__main__":
    keyboard.add_hotkey('`', runner, suppress=True)
    keyboard.wait('ctrl+esc')
