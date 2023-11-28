from statemachine import StateMachine, State
import pyaudio
from core import AudioPlayer, AudioRecorder
from core.InputOutputSelector import InputOutputSelector
import threading

class WeddingBookMachine(StateMachine):

    is_picked_up = threading.Event()
    __dev_index = InputOutputSelector().load()
    __audio = pyaudio.PyAudio()  # create pyaudio instantiation
    recorder = AudioRecorder.AudioRecoder(__audio, __dev_index, is_picked_up)
    player = AudioPlayer.AudioPlayer(__audio, __dev_index, is_picked_up)

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
        self.player.play("resources/announcement/Ansage.wav")

    def on_record(self):
        # Record guest-book entry
        self.recorder.record()
        if self.is_picked_up.is_set():
           self.player.play("resources/announcement/Aufgelegt.wav")
           self.player.play("resources/announcement/Tote_Leitung.wav")


    def on_save_recording(self):
        # Save REcording
        self.recorder.save()


    def on_pick_up(self):
        self.is_picked_up.set()
        if not self.current_state == WeddingBookMachine.idling:
            return
        try:
            self.record()
        except OSError:
            InputOutputSelector().select_device().save()


    def on_hang_up(self):
        print("Hang up")
        self.is_picked_up.clear()
        self.save_recording()
        self.complete()

