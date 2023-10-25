import pyaudio
import wave
from datetime import datetime
import threading

class Recoder:

    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    record_secs = 10 # seconds to record
    dev_index = 2 # device index found by p.get_device_info_by_index(ii)

    def __init__(self):
        self.__frames = []
        self.__recording = False

    def record(self, stream):
        print("recording")
        # loop through stream and append audio chunks to frame array
        self.__recording = True
        while self.__recording:
            data = stream.read(self.chunk)
            self.__frames.append(data)

    def save(self, audio):
        wav_output_filename = f'{datetime.now()}.wav' # name of .wav file
        print("finished recording")
        # save the audio frames as .wav file
        wavefile = wave.open(wav_output_filename,'wb')
        wavefile.setnchannels(self.chans)
        wavefile.setsampwidth(audio.get_sample_size(self.form_1))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(self.__frames))
        wavefile.close()

    def run(self):
        audio = pyaudio.PyAudio()  # create pyaudio instantiation
        # create pyaudio stream
        stream = audio.open(format=self.form_1, rate=self.samp_rate, channels=self.chans, \
                            input_device_index=self.dev_index, input=True, \
                            frames_per_buffer=self.chunk)
        record_thread = threading.Thread(target=self.record, args=(stream,))
        record_thread.start()

        stop_command =  input("Type c to stop!")
        while not stop_command == 'c':
            stop_command =  input("Type c to stop!")
        self.__recording = False
        record_thread.join()
        # stop the stream, close it, and terminate the pyaudio instantiation
        stream.stop_stream()
        stream.close()
        audio.terminate()
        self.save(audio)
        self.__frames = []