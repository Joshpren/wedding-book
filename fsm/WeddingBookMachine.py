from statemachine import StateMachine, State
from core import AudioPlayer, AudioRecorder
from core.InputOutputSelector import InputOutputSelector
import threading
import logging

logging.basicConfig(filename="logging/ weddingbook.out",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running Urban Planning")

logger = logging.getLogger('urbanGUI')

class WeddingBookMachine(StateMachine):

    is_picked_up = threading.Event()
    __dev_index = InputOutputSelector().load()
    recorder = AudioRecorder.AudioRecoder(__dev_index, is_picked_up)
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
        logging.debug("Play announcement -Ansage.wav-")
        self.player.play("resources/announcement/Ansage.wav")

    def on_record(self):
        # Record guest-book entry
        try:
            self.recorder.record()
            if self.is_picked_up.is_set():
               logging.debug("Play announcement -Aufgelegt.wav-")
               self.player.play("resources/announcement/Aufgelegt.wav")
               logging.debug("Play announcement -Tote_Leitung.wav-")
               self.player.play("resources/announcement/Tote_Leitung.wav")
        except:
            logging.exception('Got exception on main handler')


    def on_save_recording(self):
        # Save Recording
        logging.debug("Save Recording")
        self.recorder.save().close()


    def on_pick_up(self):
        self.is_picked_up.set()
        if not self.current_state == WeddingBookMachine.idling:
            return

        self.record()



    def on_hang_up(self):
        print("Hang up")
        logging.debug("Hang up")
        self.is_picked_up.clear()
        self.save_recording()
        self.complete()

