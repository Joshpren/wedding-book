from statemachine import StateMachine, State
from core import AudioPlayer, AudioRecorder
import threading
import asyncio

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
        print("Play announcement")
        AudioPlayer.AudioPlayer(self.is_picked_up).play().close()

    def on_record(self):
        # Record guest-book entry
        print("Record guest-book entry")
        self.recorder.record()


    def on_save_recording(self):
        print("Save recording")
        self.recorder.save().close()


    def on_pick_up(self):
        self.is_picked_up.set()
        if not self.current_state == WeddingBookMachine.idling:
            return
        self.record()
        # if not self.recorder.is_running():
        #     print("Stopped")
        #     self.recorder.stop()
        #     self.save_recording()
        # record_task = asyncio.create_task(self.record())

    def on_hang_up(self):
        print("Hang up")
        print(self.is_picked_up.is_set())
        self.is_picked_up.clear()
        print(self.is_picked_up.is_set())
        self.save_recording()
        self.complete()

