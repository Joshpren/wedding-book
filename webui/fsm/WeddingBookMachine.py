from statemachine import StateMachine, State
from webui.core import AudioPlayer, AudioRecorder
from webui.core.InputOutputSelector import InputOutputSelector
import threading
import logging


class WeddingBookMachine(StateMachine):

    is_picked_up = threading.Event()
    __dev_index = InputOutputSelector().load()
    logger = logging.getLogger('WeddingBookMachine')
    recorder = AudioRecorder.AudioRecorder(__dev_index, is_picked_up)
    player = AudioPlayer.AudioPlayer(__dev_index, is_picked_up)

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
        self.logger.debug("Play announcement -Ansage.wav-")
        self.player.play("resources/announcement/Ansage.wav")

    def on_record(self):
        # Record guest-book entry
        try:
            self.recorder.record()
            if self.is_picked_up.is_set():
               self.player.play("resources/announcement/Aufgelegt.wav")
               self.player.play("resources/announcement/Tote_Leitung.wav")
        except:
            self.logger.exception('Got exception on main handler')


    def on_save_recording(self):
        # Save Recording
        self.logger.debug("Save Recording")
        self.recorder.save().close()


    def on_pick_up(self):
        self.logger.debug("Pick up!")
        self.is_picked_up.set()
        if not self.current_state == WeddingBookMachine.idling:
            return

        self.record()



    def on_hang_up(self):
        print("Hang up")
        self.logger.debug("Hang up")
        self.is_picked_up.clear()
        self.save_recording()
        self.complete()

