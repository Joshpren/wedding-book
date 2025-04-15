from statemachine import StateMachine, State
from core import AudioPlayer, AudioRecorder
from core.InputOutputSelector import InputOutputSelector
import threading
import logging
logger = logging.getLogger(__name__)

class WeddingBookMachine(StateMachine):

    is_picked_up = threading.Event()
    __dev_index = InputOutputSelector().load()
    
    recorder = AudioRecorder.AudioRecorder(__dev_index, is_picked_up)
    player = AudioPlayer.AudioPlayer(__dev_index, is_picked_up)

    idling = State("Idling", initial=True)
    recording = State("Recording")

    idle = recording.to(idling)
    record = idling.to(recording)


    def before_record(self):
        # Play announcement
        logger.debug("Play announcement -Ansage.wav-")
        self.player.play("resources/announcement/Ansage.wav")

    def on_record(self):
        # Record guest-book entry
        try:
            self.recorder.record()
            if self.is_picked_up.is_set():
               self.player.play("resources/announcement/Aufgelegt.wav")
               self.player.play("resources/announcement/Tote_Leitung.wav")
        except:
            logger.exception('Got exception on main handler')

    
    def after_record(self):
        print("Save Recording")
        logger.debug("Save Recording")
        self.recorder.save().close()


    def on_pick_up(self):
        logger.debug("Pick up!")
        self.is_picked_up.set()
        if not self.current_state == WeddingBookMachine.idling:
            return

        self.record()

    def on_hang_up(self):
        logger.debug("Hang up")
        self.is_picked_up.clear()
        self.idle()

