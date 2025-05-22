from fsm import WeddingBookMachine
from gpiozero import Button
import threading
import time
import logging
logger = logging.getLogger(__name__)


class WeddingBook:

    gpio_device = None
    wbm_thread = None

    def __init__(self, config):
        self.pin_number = int(config["gpio_index"])
        self.wbm = WeddingBookMachine.WeddingBookMachine(config)
        logger.debug(f"Starting with pin-number: {self.pin_number}")
        
        
    def run_by_circuit_input(self):
        while True:
            # Do nothing
            time.sleep(0.5)

    def pick_up(self):
        logger.info("The phone has been picked up! Recording-Thread will be started!")
        self.wbm_thread = threading.Thread(target=self.wbm.on_pick_up, args=())
        self.wbm_thread.start()

    def hang_up(self):
        logger.info("The phone has been hang up! Recording-Thread will be stopped!")
        self.wbm.on_hang_up()
        self.wbm_thread.join()
        

    def gpio_setup(self, gpio_device=None):
        logger.debug("Set pin-mode to GPIO.BCM.")
        self.gpio_device = Button(pin=self.pin_number, pin_factory=gpio_device)
        self.gpio_device.when_pressed = self.pick_up
        self.gpio_device.when_released = self.hang_up
        if self.gpio_device.is_active:
            self.pick_up()

    def gpio_cleanup(self):
        logger.debug("Clean up GPIO.")
        self.gpio_device.close()