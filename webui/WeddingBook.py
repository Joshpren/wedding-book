from webui.fsm import WeddingBookMachine
import RPi.GPIO as GPIO
import threading
import time
import os
import logging


class WeddingBook:

    pin_number = 17

    def __init__(self):
        # Setze den Pin-Modus auf GPIO.BCM
        GPIO.setmode(GPIO.BCM)

        # Setze den Pin als Eingang
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
            if GPIO.input(self.pin_number) == GPIO.LOW and not is_picked_up:
                # Circuit is closed, phone has been picked up
                is_picked_up = True
                time.sleep(1)
                wbm_thread = threading.Thread(target=wbm.on_pick_up, args=())
                wbm_thread.start()
            elif not GPIO.input(self.pin_number) == GPIO.LOW and is_picked_up:
                # Circuit is interrupted
                wbm.on_hang_up()
                wbm_thread.join()
                is_picked_up = False
            else:
                # Do nothing
                time.sleep(0.5)
                pass




def setup_logging():
    # Definiere den Dateipfad
    file_path = "logging/weddingbook.log"

    # Extrahiere das Verzeichnis aus dem Dateipfad
    directory = os.path.dirname(file_path)

    # Überprüfe, ob das Verzeichnis existiert, und erstelle es, wenn nicht
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Das Verzeichnis {directory} wurde erstellt.")

    # Überprüfe, ob die Datei bereits existiert
    if not os.path.exists(file_path):
        # Wenn nicht, erstelle die Datei und öffne sie im Schreibmodus (w)
        with open(file_path, 'w'):
            # Füge optional eine Startnachricht hinzu
            print(f"Die Datei {file_path} wurde erstellt.")
    else:
        print(f"Die Datei {file_path} existiert bereits.")
        
    logging.basicConfig(filename=file_path, level=logging.DEBUG, filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S',)

setup_logging()

# try:
#     setup_logging()
#     wb = WeddingBook()
#     # run_by = input("Run by: \n [1] Keyboard Input \n [2] Circuit Input \n Enter 1 or 2.")
#     # if run_by == '1':
#     #     wb.run_by_keyboard_input()
#     # elif run_by == '2':
#     wb.run_by_circuit_input()
#     # else:
#     #     print("No valid input. Program has been stopped!")


# except KeyboardInterrupt:
#     GPIO.cleanup()


