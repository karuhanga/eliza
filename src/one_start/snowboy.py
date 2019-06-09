from libs.snowboy import snowboydecoder
import signal


class HotWordDetector:
    interrupted = False
    routines = {}
    detector = None

    def __init__(self, routines):
        # capture SIGINT signal, e.g., Ctrl+C
        # signal.signal(signal.SIGINT, self.signal_handler)
        self.sensitivity = [0.5]*len(routines)
        self.routines = routines

    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        from app.views import get_keyword_terminate
        return get_keyword_terminate()

    def listen(self, message="Snowboy is listening..."):
        print(message)
        self.detector = snowboydecoder.HotwordDetector(
            [routine['model'] for routine in self.routines],
            sensitivity=[routine['sensitivity'] for routine in self.routines]
        )
        self.detector.start(
            detected_callback=[lambda: self.cleanup_wrapper(routine['callback']) for routine in self.routines],
            interrupt_check=self.interrupt_callback,
            sleep_time=0.03
        )
        self.terminate()

    def terminate(self):
        self.detector.terminate()

    def cleanup_wrapper(self, action):
        self.terminate()
        action()
        # from src.main import listen_for_keyword
        # listen_for_keyword()
