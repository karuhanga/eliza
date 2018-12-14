import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Google Cloud Speech
try:
    print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, language="en-KE", preferred_phrases=["save", "pause", "close"]))
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))
