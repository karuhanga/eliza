from .consumers import send_message


def socket(action, errored=False):
    return lambda: send_message(action, errored)
