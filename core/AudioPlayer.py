import wave
import pyaudio
import logging

logging.basicConfig(filename="logging/weddingbook.out",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

class AudioPlayer:

    chunk = 1024

    def __init__(self, dev_index, is_picked_up):
        """ Init audio stream """
        self.__dev_index = dev_index
        self.__is_picked_up = is_picked_up
        self.__audio = pyaudio.PyAudio()

    def play(self, file):
        """ Play entire file """
        print("Play announcement")
        logging.debug("Play announcement \"{file}\"")
        try:
            wf = wave.open(file, 'rb')
            data = wf.readframes(self.chunk)
            stream = self.__audio.open(
                format=self.__audio.get_format_from_width(self.__wf.getsampwidth()),
                channels=wf.getnchannels(),
                input_device_index=self.__dev_index,
                rate=wf.getframerate(),
                output=True
            )
            while data != b'' and self.__is_picked_up.is_set():
                stream.write(data)
                data = wf.readframes(self.chunk)
        except:
            logging.exception('Got exception on main handler')
        finally:
            stream.stop_stream()
            stream.close()
            wf.close()

