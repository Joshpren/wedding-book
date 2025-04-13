from fsm import WeddingBookMachine
from gpiozero import GPIODevice
import threading
import time
import logging
logger = logging.getLogger(__name__)


class WeddingBook:

    pin_number = 17
    gpio_device = None

    def __init__(self):
        logger.debug(f"Starting with pin-number: {self.pin_number}")
        
    def run_by_keyboard_input(self):
        logger.debug("Run by keyboard input.")
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
            if self.gpio_device.value == 0 and not is_picked_up:
                # Circuit is closed, phone has been picked up
                is_picked_up = True
                time.sleep(1)
                wbm_thread = threading.Thread(target=wbm.on_pick_up, args=())
                wbm_thread.start()
            elif self.gpio_device.value == 1 and is_picked_up:
                # Circuit is interrupted
                wbm.on_hang_up()
                wbm_thread.join()
                is_picked_up = False
            else:
                # Do nothing
                time.sleep(0.5)


    def gpio_setup(self, gpio_device=GPIODevice(pin_factory=None)):
        logger.debug("Set pin-mode to GPIO.BCM.")
        self.gpio_device.pin = self.pin_number
        self.gpio_device = gpio_device

    def gpio_cleanup(self):
        logger.debug("Clean up GPIO.")
        self.gpio_device.close()