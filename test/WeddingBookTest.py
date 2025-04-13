import unittest
from WeddingBook import WeddingBook
from gpiozero import Device, Button
from gpiozero.pins.mock import MockFactory
from time import sleep


class MyTestCase(unittest.TestCase):

    def test_something(self):
        Device.pin_factory  = MockFactory()
        gpio_pin = Device.pin_factory.pin(17)
        wedding_book = WeddingBook()
        wedding_book.gpio_setup()

        gpio_device = wedding_book.gpio_device
        
        gpio_pin.drive_low()
        sleep(2)
        gpio_pin.drive_high()
        sleep(4)
        print(gpio_device.is_active)
        


        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
