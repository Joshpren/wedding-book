from fsm import WeddingBookMachine
import RPi.GPIO as GPIO
import threading

class WeddingBook:

    def run_by_keyboard_input(self):
        wbm = WeddingBookMachine.WeddingBookMachine()

        while True:
            circuit_closed = input("Record? (y)es/(n)o") == 'y'
            if circuit_closed:
                wbm_thread = threading.Thread(target=wbm.on_pick_up, args=())
                wbm_thread.start()
            else:
                wbm.on_hang_up()

    def run_by_circuit_input(self):
        wbm = WeddingBookMachine.WeddingBookMachine()
        is_picked_up = False
        while True:
            if GPIO.input(pin_nummer) == GPIO.LOW and not is_picked_up:
                # Circuit is closed, phone has been picked up
                is_picked_up = True
                wbm_thread = threading.Thread(target=wbm.on_pick_up, args=())
                wbm_thread.start()
            elif not GPIO.input(pin_nummer) == GPIO.LOW and is_picked_up:
                # Circuit is interrupted
                wbm.on_hang_up()
                is_picked_up = False
            else:
                # Do nothing
                pass



# Setze den Pin-Modus auf GPIO.BCM
GPIO.setmode(GPIO.BCM)

# Definiere den Pin, den du überwachen möchtest
pin_number = 17

# Setze den Pin als Eingang
GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)


try:
    wb = WeddingBook()
    run_by = input("Run by: \n [1] Keyboard Input \n [2] Circuit Input \n Enter 1 or 2.")
    if run_by == '1':
        wb.run_by_keyboard_input()
    elif run_by == '2':
        wb.run_by_circuit_input()
    else:
        print("No valid input. Program has been stopped!")


except KeyboardInterrupt:
    GPIO.cleanup()



