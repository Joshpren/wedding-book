import os
import wave
import pyaudio
import time

from datetime import datetime


class AudioRecoder:

    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    max_audio_length = 600 # max seconds to record

    def __init__(self, audio, dev_index, is_picked_up, storage_directory='resources/target'):
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
                self.__duration = time.time() - start_time
                return

            data = stream.read(self.chunk)
            self.__frames.append(data)

        self.__duration = time.time() - start_time
        # Recording has been stopped -> stop stream
        stream.stop_stream()
        stream.close()
        return self

    def save(self):
        """ Save the file """
        if not self.__frames or self.__duration < 5:
            # Recording is too short and wont be saved
            print("Recording is to short to be saved! It hast to be at least 5 seconds")
            return self

        print("Save recording")
        if not os.path.exists(self.__storage_directory):
            os.makedirs(self.__storage_directory)
        wav_output_filename = f'{self.__storage_directory}/{datetime.now()}.wav' # name of .wav file
        # save the audio frames as .wav file
        wavefile = wave.open(wav_output_filename,'wb')
        wavefile.setnchannels(self.chans)
        wavefile.setsampwidth(self.__audio.get_sample_size(self.form_1))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(self.__frames))
        wavefile.close()
        return self

    def close(self):
        """ Graceful shutdown """
        self.__frames = []