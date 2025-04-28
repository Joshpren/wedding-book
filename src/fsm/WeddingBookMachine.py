from statemachine import StateMachine, State
from core import AudioPlayer, AudioRecorder
from core.InputOutputSelector import InputOutputSelector
import threading
import logging
logger = logging.getLogger(__name__)

class WeddingBookMachine(StateMachine):

    is_picked_up = threading.Event()

    idling = State("Idling", initial=True)
    recording = State("Recording")

    idle = recording.to(idling)
    record = idling.to(recording)

    def __init__(self, config, model = None, state_field = "state", start_value = None, rtc = True, allow_event_without_transition = False, listeners = None):
        super().__init__(model, state_field, start_value, rtc, allow_event_without_transition, listeners)
        device_index = int(config["device_index"])
        self.recorder = AudioRecorder.AudioRecorder(device_index, self.is_picked_up)
        self.player = AudioPlayer.AudioPlayer(device_index, self.is_picked_up)


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
        self.recorder.save().close()


    def on_pick_up(self):
        if self.current_state == WeddingBookMachine.recording:
            return
        logger.debug("Pick up!")
        self.is_picked_up.set()
        self.record()

    def on_hang_up(self):
        if self.current_state == WeddingBookMachine.idling:
            return
        logger.debug("Hang up")
        self.is_picked_up.clear()
        self.idle()

