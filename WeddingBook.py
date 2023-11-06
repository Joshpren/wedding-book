from fsm import WeddingBookMachine
import threading
# import RPi.GPIO as GPIO

class WeddingBook:

    def run(self):
        wbm = WeddingBookMachine.WeddingBookMachine()

        while True:
            circuit_closed = input("Record? (y)es/(n)o") == 'y'
            if circuit_closed:
                wbm_thread = threading.Thread(target=wbm.on_pick_up, args=())
                wbm_thread.start()
            else:
                wbm.on_hang_up()


wb = WeddingBook()
wb.run()
