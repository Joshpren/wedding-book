import wave
import pyaudio
import logging

class AudioPlayer:

    chunk = 1024

    def __init__(self, dev_index, is_picked_up):
        """ Init audio stream """
        self.logger = logging.getLogger('AudioRecoder')
        self.__dev_index = dev_index
        self.__is_picked_up = is_picked_up
        self.__audio = pyaudio.PyAudio()

    def play(self, file):
        """ Play entire file """
        print("Play announcement")
        self.logger.debug(f"Play announcement \"{file}\"")
        try:
            wf = wave.open(file, 'rb')
            data = wf.readframes(self.chunk)
            stream = self.__audio.open(
                format=self.__audio.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                input_device_index=self.__dev_index,
                rate=wf.getframerate(),
                output=True
            )
            while data != b'' and self.__is_picked_up.is_set():
                stream.write(data)
                data = wf.readframes(self.chunk)
        except:
            self.logger.critical('Got exception on main handler')
        finally:
            if stream:
                stream.stop_stream()
                self.logger.debug("Stream has been stopped!")
                stream.close()
                self.logger.debug("Stream has been closed!")
            wf.close()
            self.logger.debug("Wave-File has been closed!")

