import pyaudio
import wave
from core.InputOutputSelector import InputOutputSelector

class AudioPlayer:
    chunk = 1024
    dev_index = InputOutputSelector().load()

    def __init__(self, is_picked_up, file="resources/announcement/Ansage.wav"):
        """ Init audio stream """
        self.__wf = wave.open(file, 'rb')
        self.__audio = pyaudio.PyAudio()
        self.__stream = self.__audio.open(
            format = self.__audio.get_format_from_width(self.__wf.getsampwidth()),
            channels = self.__wf.getnchannels(),
            input_device_index=self.dev_index,
            rate = self.__wf.getframerate(),
            output = True
        )
        self.__is_picked_up = is_picked_up

    def play(self):
        """ Play entire file """
        print("Play announcement")
        data = self.__wf.readframes(self.chunk)
        while data != b'' and self.__is_picked_up.is_set():
            self.__stream.write(data)
            data = self.__wf.readframes(self.chunk)
        return self


    def close(self):
        """ Graceful shutdown """
        self.__stream.close()
        self.__audio.terminate()

