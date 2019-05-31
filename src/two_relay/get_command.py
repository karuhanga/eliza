import speech_recognition as sr
from httplib2 import ServerNotFoundError

from src.two_relay.custom_recognizers import RecognizerWithDeepSpeech
from src.utils.constants import COMMAND_SCOPE


r = None


def get_command(command_scope=None, message="Listening..."):
    global r
    if not r:
        r = RecognizerWithDeepSpeech()
    if command_scope is None:
        command_scope = []
    with sr.Microphone(sample_rate=16000) as source:
        print(message)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Wait timeout")
            return

    print("Recognizing...")

    try:
        return r.recognize_deep_speech(audio)
        # return r.recognize_google_cloud(audio, language="en-KE").strip()
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
    except ServerNotFoundError:
        print("You are offline at the moment")


if __name__ == "__main__":
    command = get_command(command_scope=COMMAND_SCOPE)
    if command:
        print(command)
    else:
        print("Failed to recognize word")
