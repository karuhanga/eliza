import speech_recognition as sr
from httplib2 import ServerNotFoundError

from src.relays.custom_recognizers import RecognizerWithDeepSpeech
from src.utils.constants import COMMAND_SCOPE


r = RecognizerWithDeepSpeech()


def get_command(command_scope=None, message="Listening..."):
    if command_scope is None:
        command_scope = []
    with sr.Microphone() as source:
        print(message)
        try:
            audio = r.listen(source, timeout=2, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Wait timeout")
            return

    print("Recognizing...")

    try:
        # print(r.recognize_deep_speech(audio))
        return r.recognize_google_cloud(audio, language="en-KE").strip()
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
