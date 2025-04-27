from fsm import WeddingBookMachine
from gpiozero import Button
import threading
import time
import logging
logger = logging.getLogger(__name__)


class WeddingBook:

    gpio_device = None
    __wbm_thread = None

    def __init__(self, config):
        self.pin_number = int(config["gpio_index"])
        self.__wbm = WeddingBookMachine.WeddingBookMachine(config)
        logger.debug(f"Starting with pin-number: {self.pin_number}")
        
        
    def run_by_circuit_input(self):
        while True:
            # Do nothing
            time.sleep(0.5)

    def pick_up(self):
        self.__wbm_thread = threading.Thread(target=self.__wbm.on_pick_up, args=())
        self.__wbm_thread.start()

    def hang_up(self):
        self.__wbm.on_hang_up()
        self.__wbm_thread.join()
        

    def gpio_setup(self, gpio_device=None):
        logger.debug("Set pin-mode to GPIO.BCM.")
        self.gpio_device = Button(pin=self.pin_number, pin_factory=gpio_device)
        self.gpio_device.when_pressed = self.pick_up
        self.gpio_device.when_released = self.hang_up

    def gpio_cleanup(self):
        logger.debug("Clean up GPIO.")
        self.gpio_device.close()