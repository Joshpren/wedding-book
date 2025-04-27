import unittest
from WeddingBook import WeddingBook
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from time import sleep


class MyTestCase(unittest.TestCase):

    def test_recording(self):
        Device.pin_factory  = MockFactory()
        gpio_pin = Device.pin_factory.pin(17)
        config = { "gpio_index":17, "device_index": 1 }
        wedding_book = WeddingBook(config)
        wedding_book.gpio_setup()

        gpio_device = wedding_book.gpio_device
        
        # Initial state
        self.assertEqual(False, gpio_device.is_active)
        sleep(2)
        # Pick up
        print("Pick up")
        gpio_pin.drive_low()
        self.assertEqual(True, gpio_device.is_active)
        sleep(2)
        # Hang up
        print("Hang up")
        gpio_pin.drive_high()
        self.assertEqual(False, gpio_device.is_active)
        

if __name__ == '__main__':
    unittest.main()
