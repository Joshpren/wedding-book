from datetime import datetime
import json
import os
import pyaudio
from statemachine import StateMachine, State
import RPi.GPIO as GPIO
import threading
import time
import wave


class InputOutputSelector:

    config_path = 'resources/config/config.json'

    def __init__(self):
        self.__prefered_device = None

    def select_device(self):
        py_audio = pyaudio.PyAudio()
        for ii in range(py_audio.get_device_count()):
            device_info = py_audio.get_device_info_by_index(ii)
            device_name = device_info.get('name')
            print(f"ID: {ii} - Name: {device_name}")
        self.__prefered_device = int(input())
        return self

    def save(self):
        dictionary = {
            "dev_index": self.__prefered_device
        }
        # Serializing json
        json_object = json.dumps(dictionary, indent=1)

        # Writing to sample.json
        with open(self.config_path, "w") as outfile:
            outfile.write(json_object)

    def load(self):
        with open(self.config_path, 'r') as openfile:
            json_object = json.load(openfile)
        return int(json_object["dev_index"])


class AudioPlayer:
    chunk = 1024

    def __init__(self, is_picked_up, file="resources/announcement/Ansage.wav"):
        """ Init audio stream """
        self.__wf = wave.open(file, 'rb')
        self.__audio = pyaudio.PyAudio()
        self.__stream = self.__audio.open(
            format = self.__audio.get_format_from_width(self.__wf.getsampwidth()),
            channels = self.__wf.getnchannels(),
            rate = self.__wf.getframerate(),
            output = True
        )
        self.__is_picked_up = is_picked_up

    def play(self):
        """ Play entire file """
        print("Play announcement")
        data = self.__wf.readframes(self.chunk)
        while data != b'' and self.__is_picked_up.is_set():
            self.__stream.write(data)
            data = self.__wf.readframes(self.chunk)
        return self


    def close(self):
        """ Graceful shutdown """
        self.__stream.close()
        self.__audio.terminate()


class AudioRecoder:

    form_1 = pyaudio.paInt16 # 16-bit resolution
    chans = 1 # 1 channel
    samp_rate = 44100 # 44.1kHz sampling rate
    chunk = 4096 # 2^12 samples for buffer
    max_audio_length = 600 # max seconds to record
    dev_index = InputOutputSelector().load() # device index found by p.get_device_info_by_index(ii)


    def __init__(self, is_picked_up, storage_directory='resources/target'):
        self.__storage_directory = storage_directory
        self.__audio = pyaudio.PyAudio()  # create pyaudio instantiation
        self.__stream = None
        self.__frames = []
        self.__duration = 0
        self.__is_picked_up = is_picked_up

    def record(self):
        """ Record audio """
        if not self.__is_picked_up:
            return
        print("recording")
        # Open audio stream
        self.__stream = self.__audio.open(format=self.form_1, rate=self.samp_rate, channels=self.chans, \
                                          input_device_index=self.dev_index, input=True, \
                                          frames_per_buffer=self.chunk)
        # Start timer
        start_time = time.time()
        while self.__is_picked_up.is_set():
            if int(time.time() - start_time) >= self.max_audio_length:
                # if duration reaches max audio length, then stop recording
                print(f"Recording has been stopped after exceeding the maximum length of {self.max_audio_length} seconds!")
                self.__duration = time.time() - start_time
                return

            data = self.__stream.read(self.chunk)
            self.__frames.append(data)

        self.__duration = time.time() - start_time
        # Recording has been stopped -> stop stream
        self.__stream.stop_stream()
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
        # if self.__audo:
        #     self.__audio.terminate()
        if self.__stream:
            self.__stream.close()


class WeddingBookMachine(StateMachine):

    is_picked_up = threading.Event()
    recorder = AudioRecoder(is_picked_up)


    idling = State("Idling", initial=True)
    recording = State("Recording")
    saving = State("Saving")
    canceling = State("Canceling")

    idle = idling.to.itself()
    record = idling.to(recording)
    cancel = canceling.from_(recording, idling)
    save_recording = recording.to(saving)
    complete = saving.to(idling)


    def before_record(self):
        # Play announcement
        AudioPlayer(self.is_picked_up).play().close()

    def on_record(self):
        # Record guest-book entry
        self.recorder.record()
        if self.is_picked_up.is_set():
            AudioPlayer(self.is_picked_up, "resources/announcement/Aufgelegt.wav").play().close()
            AudioPlayer(self.is_picked_up, "resources/announcement/Tote_Leitung.wav").play().close()


    def on_save_recording(self):
        # Save REcording
        self.recorder.save().close()


    def on_pick_up(self):
        self.is_picked_up.set()
        if not self.current_state == WeddingBookMachine.idling:
            return
        self.record()

    def on_hang_up(self):
        print("Hang up")
        self.is_picked_up.clear()
        self.save_recording()
        self.complete()

class WeddingBook:

    pin_number = 17

    def __init__(self):
        # Setze den Pin-Modus auf GPIO.BCM
        GPIO.setmode(GPIO.BCM)

        # Setze den Pin als Eingang
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def run_by_keyboard_input(self):
        wbm = WeddingBookMachine.WeddingBookMachine(dev_index)

        while True:
            circuit_closed = input("Record? (y)es/(n)o") == 'y'
            if circuit_closed:
                wbm_thread = threading.Thread(target=wbm.on_pick_up, args=())
                wbm_thread.start()
            else:
                wbm.on_hang_up()

    def run_by_circuit_input(self):
        wbm = WeddingBookMachine()
        is_picked_up = False
        while True:
            if GPIO.input(self.pin_number) == GPIO.LOW and not is_picked_up:
                # Circuit is closed, phone has been picked up
                is_picked_up = True
                time.sleep(1)
                wbm_thread = threading.Thread(target=wbm.on_pick_up, args=())
                wbm_thread.start()
            elif not GPIO.input(self.pin_number) == GPIO.LOW and is_picked_up:
                # Circuit is interrupted
                wbm.on_hang_up()
                wbm_thread.join()
                is_picked_up = False
            else:
                # Do nothing
                time.sleep(0.5)
                pass


try:
    wb = WeddingBook()
    wb.run_by_circuit_input()
except KeyboardInterrupt:
    GPIO.cleanup()



