from statemachine import StateMachine, State
from time import sleep
from fsm import Recorder

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
        for i in range(10):
            print("Grüne Led blinkt")
            sleep(0.5)
        self.send("record")

    def on_record(self):
        Recorder.record()
        self.send("save_recording")

    def on_save_recording(self):
        print("Save")
        self.send("finish")

sm = WeddingBookMachine()
# print([t.name for t in sm.events])
while True:
    sm.send("idle")
# sm.send("record_entry")

