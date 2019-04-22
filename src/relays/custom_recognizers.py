import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from speech_recognition import Recognizer, AudioData, RequestError, UnknownValueError


class RecognizerWithKaldi(Recognizer):
    """
    Recognizer class with a recognize_kaldi method added
    Inspiration from https://github.com/Uberi/speech_recognition/pull/122
    """

    def recognize_kaldi(self, audio_data, host, show_all=False):
        """
        Performs speech recognition on ``audio_data`` (an ``AudioData`` instance),
        using the http POST api for kaldi-gstreamer-server.
        Returns the most likely transcription if ``show_all`` is false (the default).
        Otherwise, returns the raw API response as a JSON dictionary.
        Raises a ``speech_recognition.UnknownValueError`` exception if the speech
        is unintelligible. Raises a ``speech_recognition.RequestError`` exception
        if the speech recognition operation failed,  or if there is no internet connection.
        """
        assert isinstance(audio_data, AudioData), "`audio_data` must be audio data"
        assert isinstance(host, str), "`host` must be a string"
        response_status = {
            0: "Success.",
            2: "Aborted.",
            1: "No speech.",
            5: "Internal data flow error.",
            9: "Not available."
        }
        url = "http://{0}/client/dynamic/recognize".format(host)
        content_type = ("audio/x-raw-int;rate={0}").format(audio_data.sample_rate)
        request = Request(url, data=audio_data.get_raw_data(), headers={
            "Content-Type": content_type})
        # obtain audio transcription results
        try:
            response = urlopen(request)
        except HTTPError as e:
            # use getattr to be compatible with Python 2.6
            raise RequestError(
                "recognition request failed: {0}".format(getattr(e, "reason", "status {0}".format(e.code))))
        except URLError as e:
            raise RequestError("recognition connection failed: {0}".format(e.reason))
        response_text = response.read().decode("utf-8")
        actual_result = json.loads(response_text)
        status = int(actual_result['status'])
        if status not in (0, 1):
            raise RequestError("Server returned: {0} - {1} ".format(status, response_status[status]))
        if "hypotheses" in actual_result:
            result = actual_result["hypotheses"]
        if show_all:
            return actual_result
        for entry in result:
            if "utterance" in entry:
                return entry["utterance"]
        raise UnknownValueError()  # no transcriptions available
