from src.two_relay.get_command import get_command


def listen(message):
    command = get_command(message=message)
    if command:
        return command
    print("Sorry, I didn't get that")
