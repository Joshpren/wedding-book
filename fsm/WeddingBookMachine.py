from statemachine import StateMachine, State
from time import sleep
from core import AudioPlayer, AudioRecorder
import threading

class WeddingBookMachine(StateMachine):

    recorder = AudioRecorder.AudioRecoder()
    idling = State("Idling", initial=True)
    recording = State("Recording", rec=recorder)
    saving = State("Saving", rec=recorder)
    canceling = State("Canceling")

    idle = idling.to.itself()
    record = idling.to(recording)
    cancel = canceling.from_(record, idling)
    save_recording = recording.to(saving)
    finish = saving.to(idling)


    def on_idle(self):
        i = input("Sag was")
        while not i  == 's':
            i = input("Sag was")
        self.send("record")


    def before_record(self):
        # for i in range(2):
        #     print("Grüne Led blinkt")
        #     sleep(0.5)
        # Play announcement
        AudioPlayer.AudioPlayer("resources/announcement/Aufzeichnung.wav").play().close()

    def on_record(self):

        self.rec.record()
        self.send("save_recording")
        # stop_command = input("Type c to stop!")
        # while not stop_command == 'c':
        #     stop_command = input("Type c to stop!")
        # recorder.stop_recording()

    def on_save_recording(self):
        print("Save")
        self.rec.save().close()
        self.send("finish")


    def on_pick_up(self):
        if not self.current_state == WeddingBookMachine.idling:
            return
        self.send("record")

    def on_hang_up(self):
        if self.current_state == WeddingBookMachine.idling:
            return
        elif self.current_state == WeddingBookMachine.recording:
            self.recorder.stop_recording()



# sm = WeddingBookMachine()
# # record_thread = threading.Thread(target=recorder.record, args=())
# # record_thread.start()
# # record_thread.join()
# while True:
#     sm.send("idle")

