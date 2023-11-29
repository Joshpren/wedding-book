import wave
import pyaudio

class AudioPlayer:

    chunk = 1024

    def __init__(self, audio, dev_index, is_picked_up):
        """ Init audio stream """
        self.__dev_index = dev_index
        self.__is_picked_up = is_picked_up
        self.__audio = pyaudio.PyAudio()

    def play(self, file):
        """ Play entire file """
        print("Play announcement")

        self.__wf = wave.open(file, 'rb')
        data = self.__wf.readframes(self.chunk)
        stream = self.__audio.open(
            format=self.__audio.get_format_from_width(self.__wf.getsampwidth()),
            channels=self.__wf.getnchannels(),
            input_device_index=self.__dev_index,
            rate=self.__wf.getframerate(),
            output=True
        )
        while data != b'' and self.__is_picked_up.is_set():
            stream.write(data)
            data = self.__wf.readframes(self.chunk)
        stream.stop_stream()
        stream.close()

