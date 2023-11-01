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
    record_secs = 10 # seconds to record
    dev_index = 2 # device index found by p.get_device_info_by_index(ii)
    max_audio_length = 600

    def __init__(self, storage_directory = 'resources/target'):
        self.__storage_directory = storage_directory
        self.__audio = pyaudio.PyAudio()  # create pyaudio instantiation
        self.__stream = None
        self.__frames = []
        self.__duration = 0
        self.__recording = False


    def record(self):
        """ Record audio """
        print("recording")
        # Open audio stream
        self.__stream = self.__audio.open(format=self.form_1, rate=self.samp_rate, channels=self.chans, \
                                          input_device_index=self.dev_index, input=True, \
                                          frames_per_buffer=self.chunk)
        # Start timer
        start_time = time.time()
        self.__recording = True
        while self.__recording:
            if int(time.time() - start_time) >= self.max_audio_length:
                # if duration reaches max audio length, then stop recording
                self.__recording = False

            data = self.__stream.read(self.chunk)
            self.__frames.append(data)

        self.__duration = time.time() - start_time
        # Recording has been stopped -> stop stream
        self.__stream.stop_stream()

        return self

    def save(self):
        """ Save the file """
        print("Save recording")
        if self.__duration < 5:
            # Recording is too short and wont be saved
            return self

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
        # if self.__audo:
        #     self.__audio.terminate()
        if self.__stream:
            self.__stream.close()


    def stop_recording(self):
        self.__recording = False

