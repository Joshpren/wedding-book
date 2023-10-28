import pyaudio
import wave

class AudioPlayer:
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """
        self.__wf = wave.open(file, 'rb')
        self.__audio = pyaudio.PyAudio()
        self.__stream = self.__audio.open(
            format = self.__audio.get_format_from_width(self.__wf.getsampwidth()),
            channels = self.__wf.getnchannels(),
            rate = self.__wf.getframerate(),
            output = True
        )

    def play(self):
        """ Play entire file """
        data = self.__wf.readframes(self.chunk)
        while data != b'':
            self.__stream.write(data)
            data = self.__wf.readframes(self.chunk)

        return self

    def close(self):
        """ Graceful shutdown """
        self.__stream.close()
        self.__audio.terminate()

