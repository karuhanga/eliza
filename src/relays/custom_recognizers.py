import io
import json
import wave
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import numpy
from deepspeech import Model as DeepSpeechModel
from deepspeech.client import N_FEATURES, N_CONTEXT, BEAM_WIDTH, LM_ALPHA, \
    LM_BETA

from speech_recognition import Recognizer, AudioData, RequestError, UnknownValueError

from libs.deep_speech.constants import MODEL_PATH, ALPHABET_PATH, \
    LANGUAGE_MODEL, TRIE


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


class RecognizerWithDeepSpeech(Recognizer):
    def __init__(self):
        super(RecognizerWithDeepSpeech, self).__init__()
        self.deep_speech_model = DeepSpeechModel(MODEL_PATH, N_FEATURES, N_CONTEXT, ALPHABET_PATH, BEAM_WIDTH)
        self.deep_speech_model.enableDecoderWithLM(ALPHABET_PATH, LANGUAGE_MODEL, TRIE, LM_ALPHA, LM_BETA)

    def get_wav_data(self, audio_data, convert_rate=None, convert_width=None):
        raw_data = audio_data.get_raw_data(convert_rate, convert_width)
        sample_rate = audio_data.sample_rate if convert_rate is None else convert_rate
        sample_width = audio_data.sample_width if convert_width is None else convert_width

        # generate the WAV file contents
        with io.BytesIO() as wav_file:
            with wave.open(wav_file, "wb") as wav_writer:
                try:  # note that we can't use context manager, since that was only added in Python 3.4
                    wav_writer.setframerate(sample_rate)
                    wav_writer.setsampwidth(sample_width)
                    wav_writer.setnchannels(1)
                    wav_writer.writeframes(raw_data)
                    wav_file.seek(0)
                finally:  # make sure resources are cleaned up
                    wav_writer.close()

            with wave.open(wav_file, 'rb') as wav_reader:
                audio = numpy.frombuffer(wav_reader.readframes(wav_reader.getnframes()),
                        numpy.int16)
                frame_rate = wav_reader.getframerate()

        return frame_rate, audio

    def recognize_deep_speech(self, audio_data):
        """
        Performs speech recognition on ``audio_data`` (an ``AudioData`` instance), using the Mozilla Deep Speech Library.
        """
        assert isinstance(audio_data, AudioData), "Data must be audio data"
        frame_rate, audio = self.get_wav_data(
            audio_data,
            # audio samples should be at least 16 kHz
            convert_rate=None if audio_data.sample_rate >= 16000 else 16000,
            # audio samples should be at least 16-bit
            convert_width=None if audio_data.sample_width >= 2 else 2
        )

        return self.deep_speech_model.stt(audio, frame_rate)
