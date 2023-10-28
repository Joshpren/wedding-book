import pyaudio
import wave
from datetime import datetime


class AudioRecoder:

    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    record_secs = 10 # seconds to record
    dev_index = 1 # device index found by p.get_device_info_by_index(ii)

    def __init__(self):
        self.__audio = pyaudio.PyAudio()  # create pyaudio instantiation
        self.__stream = self.__audio.open(format=self.form_1, rate=self.samp_rate, channels=self.chans, \
                                   input_device_index=self.dev_index, input=True, \
                                   frames_per_buffer=self.chunk)
        self.__frames = []
        self.__recording = False


    def record(self):
        """ Record audio """
        print("recording")

        self.__recording = True
        while self.__recording:
            data = self.__stream.read(self.chunk)
            self.__frames.append(data)
        # Recording has been stopped -> stop stream
        self.__stream.stop_stream()


        return self

    def save(self):
        """ Save the file """
        wav_output_filename = f'./../target/recordings/{datetime.now()}.wav' # name of .wav file
        print("finished recording")
        # save the audio frames as .wav file
        wavefile = wave.open(wav_output_filename,'wb')
        wavefile.setnchannels(self.chans)
        wavefile.setsampwidth(self.__audio.get_sample_size(self.form_1))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(self.__frames))
        wavefile.close()
        self.__frames = []

        return self

    def close(self):
        """ Graceful shutdown """
        self.__audio.terminate()
        self.__stream.close()


    def stop_recording(self):
        self.__recording = False

