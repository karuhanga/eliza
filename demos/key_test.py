import keyboard


def print_pressed_keys(e):
    print(e)
    line = ', '.join(str(code) for code in keyboard._pressed_events)
    # '\r' and end='' overwrites the previous line.
    # ' '*40 prints 40 spaces at the end to ensure the previous line is cleared.
    print(line)


keyboard.hook(print_pressed_keys)
keyboard.wait("ctrl+esc")
