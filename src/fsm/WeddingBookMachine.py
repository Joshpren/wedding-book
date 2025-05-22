from statemachine import StateMachine, State
from core import AudioPlayer, AudioRecorder
from core.InputOutputSelector import InputOutputSelector
import threading
import logging
logger = logging.getLogger(__name__)

class WeddingBookMachine(StateMachine):

    is_picked_up = threading.Event()

    idling = State("Idling", initial=True)
    playing = State("Playing")
    recording = State("Recording")

    idle = idling.from_(playing, recording)
    play = idling.to(playing)
    record = playing.to(recording)

    def __init__(self, config, model = None, state_field = "state", start_value = None, rtc = True, allow_event_without_transition = False, listeners = None):
        super().__init__(model, state_field, start_value, rtc, allow_event_without_transition, listeners)
        input_device_index = config["input_device_index"]
        output_device_index = config.get("output_device_index", None)
       
        max_recording_duration_in_sec = int(config["max_recording_duration_in_sec"])
        self.recorder = AudioRecorder.AudioRecorder(input_device_index, max_recording_duration_in_sec, self.is_picked_up)
        self.player = AudioPlayer.AudioPlayer(output_device_index, self.is_picked_up)


    def on_enter_playing(self):
        # Play announcement
        logger.debug("Play announcement -Ansage.wav-")
        self.player.play("resources/announcement/Ansage.wav")

    def after_play(self):
        if self.is_picked_up.is_set():
            self.record()


    def on_enter_recording(self):
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
        if(self.current_state != self.idling):
            logger.warn(f"'on-hang-up' has been called in state: {self.current_state} - But it has to be in state 'idling'")
            return
        logger.debug(f"Current State: {self.current_state} - on pick up")
        self.is_picked_up.set()
        self.play()

    def on_hang_up(self):
        if(self.current_state == self.idling):
            logger.warn(f"'on-hang-up' has been called in state: {self.current_state} - But it either has to be in state 'recording' or 'playing'")
            return
        logger.debug(f"Current State: {self.current_state} - on hang up")
        self.is_picked_up.clear()
        self.idle()

