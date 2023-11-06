from statemachine import StateMachine, State
from core import AudioPlayer, AudioRecorder
import threading

class WeddingBookMachine(StateMachine):

    is_picked_up = threading.Event()
    recorder = AudioRecorder.AudioRecoder(is_picked_up)


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
        AudioPlayer.AudioPlayer(self.is_picked_up).play().close()

    def on_record(self):
        # Record guest-book entry
        self.recorder.record()
        if self.is_picked_up.is_set():
            AudioPlayer.AudioPlayer(self.is_picked_up, "resources/announcement/Aufgelegt.wav").play().close()
            AudioPlayer.AudioPlayer(self.is_picked_up, "resources/announcement/Tote_Leitung.wav").play().close()


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

