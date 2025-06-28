from statemachine import StateMachine, State
from core import AudioPlayer, AudioRecorder
from gpiozero import Button
import threading
import logging
logger = logging.getLogger(__name__)

class WeddingBook(StateMachine):

    gpio_device = None
    is_picked_up = threading.Event()
    fsm_thread = None

    idling = State("Idling", initial=True)
    playing = State("Playing")
    recording = State("Recording")

    idle = idling.from_(playing, recording)
    play = idling.to(playing)
    record = playing.to(recording)

    def __init__(self, config, model = None, state_field = "state", start_value = None, rtc = True, allow_event_without_transition = False, listeners = None):
        super().__init__(model, state_field, start_value, rtc, allow_event_without_transition, listeners)
        self.pin_number = int(config["gpio_index"])
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
            logger.warning(f"'on-hang-up' has been called in state: {self.current_state} - But it has to be in state 'idling'")
            return
        logger.debug(f"Current State: {self.current_state} - on pick up")
        logger.info("The phone has been picked up! Recording-Thread will be started!")
        self.is_picked_up.set()
        self.fsm_thread = threading.Thread(target=self.play, args=())
        self.fsm_thread.start()

    def on_hang_up(self):
        if(self.current_state == self.idling):
            logger.warning(f"'on-hang-up' has been called in state: {self.current_state} - But it either has to be in state 'recording' or 'playing'")
            return
        logger.debug(f"Current State: {self.current_state} - on hang up")
        logger.info("The phone has been hang up! Recording-Thread will be stopped!")
        self.is_picked_up.clear()
        self.fsm_thread.join()
        self.idle()


    def gpio_setup(self, gpio_device=None):
        logger.debug("Set pin-mode to GPIO.BCM.")
        self.gpio_device = Button(pin=self.pin_number, pin_factory=gpio_device)
        self.gpio_device.when_pressed = self.on_pick_up
        self.gpio_device.when_released = self.on_hang_up
        if self.gpio_device.is_active:
            self.on_pick_up()

    def gpio_cleanup(self):
        logger.debug("Clean up GPIO.")
        self.gpio_device.close()
