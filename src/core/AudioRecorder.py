import os
import wave
import pyaudio
import time
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

class AudioRecorder:

    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 44100
    chunk = 4096

    def __init__(self, dev_index, max_recording_duration_in_sec, is_picked_up, storage_directory='resources/target'):
        
        self.__storage_directory = storage_directory
        self.__audio = pyaudio.PyAudio()
        self.__dev_index = dev_index
        self.__frames = []
        self.__duration = 0
        self.__is_picked_up = is_picked_up
        self.__max_recording_duration_in_sec = max_recording_duration_in_sec

    def record(self):
        if not self.__is_picked_up:
            return
        logger.info("Recording")
        try:
            stream = self.__audio.open(
                format=self.form_1, rate=self.samp_rate, channels=self.chans,
                input_device_index=self.__dev_index, input=True,
                frames_per_buffer=self.chunk
            )
            start_time = time.time()
            while self.__is_picked_up.is_set():
                if int(time.time() - start_time) >= self.__max_recording_duration_in_sec:
                    logger.info(f"Recording has been stopped after exceeding the maximum length of {self.__max_recording_duration_in_sec} seconds!")
                    self.__duration = time.time() - start_time
                    break
                data = stream.read(self.chunk)
                self.__frames.append(data)
            self.__duration = time.time() - start_time
        except Exception as e:
            logger.exception(f'Got exception on main handler: {e}')
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                logger.debug("Stream stopped")
                stream.close()
                logger.debug("Stream closed")
        return self

    def save(self):
        if not self.__frames or self.__duration < 5:
            logger.debug("Recording is too short to be saved! It has to be at least 5 seconds")
            return self
        logger.debug("Save recording")
        try:
            if not os.path.exists(self.__storage_directory):
                os.makedirs(self.__storage_directory)
                logger.debug(f"No directory has been found for {self.__storage_directory} and therefore has been created!")
            wav_output_filename = f'{self.__storage_directory}/{datetime.now().strftime("%Y%m%d-%H%M%S")}.wav'
            wavefile = wave.open(wav_output_filename, 'wb')
            wavefile.setnchannels(self.chans)
            wavefile.setsampwidth(self.__audio.get_sample_size(self.form_1))
            wavefile.setframerate(self.samp_rate)
            wavefile.writeframes(b''.join(self.__frames))
        except Exception as e:
            logger.critical(f'Got exception on main handler: {e}')
        finally:
            wavefile.close()
            logger.debug("Wavefile has been closed")
        return self

    def close(self):
        self.__frames = []
        logger.debug(f"Reset Frames {self.__frames}")
