from statemachine import StateMachine, State
from time import sleep
from core import AudioPlayer, AudioRecorder
import threading

class WeddingBookMachine(StateMachine):

    idling = State("Idling", initial=True)
    initializing = State("Initializing")
    recording = State("Recording")
    saving = State("Saving")
    canceling = State("Canceling")

    idle = idling.to.itself()
    initialize = idling.to(initializing)
    record = initializing.to(recording)
    cancel = canceling.from_(initializing, idling)
    save_recording = recording.to(saving)
    finish = saving.to(idling)


    def on_idle(self):
        i = input("Sag was")
        while not i  == 's':
            i = input("Sag was")
        self.send("initialize")

    def on_initialize(self):
        for i in range(5):
            print("Grüne Led blinkt")
            sleep(0.5)
        # Usage example for pyaudios
        AudioPlayer.AudioPlayer("./../resources/announcement/Aufzeichnung.wav").play().close()

        self.send("record")

    def on_record(self):
        recorder = AudioRecorder.AudioRecoder()
        record_thread = threading.Thread(target=recorder.record, args=())
        record_thread.start()
        stop_command = input("Type c to stop!")
        while not stop_command == 'c':
            stop_command = input("Type c to stop!")
        recorder.stop_recording()
        record_thread.join()
        self.send("save_recording", recorder)

    def on_save_recording(self, recorder):
        print("Save")
        recorder.save().close()
        self.send("finish")

sm = WeddingBookMachine()
# print([t.name for t in sm.events])
while True:
    sm.send("idle")
# sm.send("record_entry")

