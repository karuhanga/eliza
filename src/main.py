from libs.snowboy.snowboydecoder import play_audio_file
from src.one_start.actions.speech import eliza_action
from src.one_start.main import build_detector, build_wake_up_detector

wake_up_detector = None
detector = None


def listen_for_wake_up_word():
    global wake_up_detector, detector
    if detector:
        detector.terminate()
    wake_up_detector = build_wake_up_detector("eliza", listen_for_keyword)
    wake_up_detector.listen()


# todo: We might choose to do this asynchronously after, say, a minute
def stop_keyword_capture():
    play_audio_file()
    print("Cool.")
    listen_for_wake_up_word()


def listen_for_keyword():
    global detector, wake_up_detector
    if wake_up_detector:
        wake_up_detector.terminate()
    eliza_action()
    detector = build_detector("goodbye", stop_keyword_capture)
    detector.listen("Waiting for action...")


if __name__ == "__main__":
    listen_for_wake_up_word()
