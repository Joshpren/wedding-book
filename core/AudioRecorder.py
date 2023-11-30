import os
import wave
import pyaudio
import time
import logging
from datetime import datetime

class AudioRecoder:

    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    max_audio_length = 300 # max seconds to record

    def __init__(self, dev_index, is_picked_up, storage_directory='resources/target'):
        self.logger = logging.getLogger('AudioRecoder')
        self.__storage_directory = storage_directory
        self.__audio = pyaudio.PyAudio()  # create pyaudio instantiation
        self.__dev_index = dev_index# device index found by p.get_device_info_by_index(ii)
        self.__frames = []
        self.__duration = 0
        self.__is_picked_up = is_picked_up

    def record(self):
        """ Record audio """
        if not self.__is_picked_up:
            return
        print("recording")
        try:
            # Open audio stream
            stream = self.__audio.open(format=self.form_1, rate=self.samp_rate, channels=self.chans, \
                                              input_device_index=self.__dev_index, input=True, \
                                              frames_per_buffer=self.chunk)
            # Start timer
            start_time = time.time()
            while self.__is_picked_up.is_set():
                if int(time.time() - start_time) >= self.max_audio_length:
                    # if duration reaches max audio length, then stop recording
                    print(f"Recording has been stopped after exceeding the maximum length of {self.max_audio_length} seconds!")
                    self.logger.info(f"Recording has been stopped after exceeding the maximum length of {self.max_audio_length} seconds!")
                    self.__duration = time.time() - start_time
                    break

                data = stream.read(self.chunk)
                self.__frames.append(data)

            self.__duration = time.time() - start_time
        except Exception as e:
            self.logger.exception(e)
        finally:
            # Recording has been stopped -> stop stream
            stream.stop_stream()
            self.logger.debug("Stream stopped")
            stream.close()
            self.logger.debug("Stream closed")
        return self

    def save(self):
        """ Save the file """
        if not self.__frames or self.__duration < 5:
            # Recording is too short and wont be saved
            print("Recording is to short to be saved! It hast to be at least 5 seconds")
            self.logger.debug("Recording is to short to be saved! It hast to be at least 5 seconds")
            return self

        print("Save recording")
        self.logger.debug("Save recording")
        try:
            if not os.path.exists(self.__storage_directory):
                os.makedirs(self.__storage_directory)
                self.logger.debug(f"No directory has been found for {self.__storage_directory} and therefore has been created!")
            wav_output_filename = f'{self.__storage_directory}/{datetime.now()}.wav' # name of .wav file
            # save the audio frames as .wav file
            wavefile = wave.open(wav_output_filename,'wb')
            wavefile.setnchannels(self.chans)
            wavefile.setsampwidth(self.__audio.get_sample_size(self.form_1))
            wavefile.setframerate(self.samp_rate)
            wavefile.writeframes(b''.join(self.__frames))
        except:
            self.logger.critical(e)
        finally:
            # Close Wave-File
            wavefile.close()
            self.logger.debug("Wavefile has been closed")
        return self

    def close(self):
        """ Graceful shutdown """
        self.__frames = []
        self.logger.debug(f"Reset Frames {self.__frames}")