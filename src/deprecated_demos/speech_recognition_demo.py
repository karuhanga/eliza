import speech_recognition as sr

from src.two_relay.custom_recognizers import RecognizerWithKaldi

r = RecognizerWithKaldi()
# obtain audio from the microphone
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)


def use_google_cloud_speech_api():
    # recognize speech using Google Cloud Speech
    try:
        print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, language="en-KE",
                                                                                preferred_phrases=["save", "pause",
                                                                                                   "close"]))
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))


def use_pocket_sphinx():
    # recognize speech using Sphinx
    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


def use_kaldi():
    # recognize speech using kaldi-gstreamer-server at localhost
    kaldi_host = "localhost:8888"
    try:
        print("Kaldi thinks you said " + str(r.recognize_kaldi(audio, host=kaldi_host)))
    except sr.UnknownValueError:
        print("Kaldi could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Kaldi; {0}".format(e))


use_google_cloud_speech_api()
use_pocket_sphinx()
use_kaldi()
