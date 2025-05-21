import wave
import pyaudio
import logging
logger = logging.getLogger(__name__)

class AudioPlayer:

    chunk = 1024

    def __init__(self, dev_index, is_picked_up):
        self.__dev_index = dev_index
        self.__is_picked_up = is_picked_up
        self.__audio = pyaudio.PyAudio()

    def play(self, file):
        logger.debug(f"Play announcement \"{file}\"")
        try:
            wf = wave.open(file, 'rb')
            stream = self.__audio.open(
                format=self.__audio.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                output_device_index=self.__dev_index,
                rate=wf.getframerate(),
                output=True
            )
            data = wf.readframes(self.chunk)
            while data != b'' and self.__is_picked_up.is_set():
                stream.write(data)
                data = wf.readframes(self.chunk)
        except:
            logger.exception('Got exception on main handler')
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                logger.debug(f"Stream of \"{file}\" has been stopped!")
                stream.close()
                logger.debug(f"Stream of \"{file}\" has been closed!")
            wf.close()
            logger.debug("Wave-File has been closed!")
