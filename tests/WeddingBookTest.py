import unittest
from WeddingBook import WeddingBook
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from time import sleep


class WeddingBookMaschineTest(unittest.TestCase):


    def test_playing(self):
        print("Test Playing")
        Device.pin_factory  = MockFactory()
        gpio_pin = Device.pin_factory.pin(17)
        config = { "gpio_index":17, "device_index": 1 }
        wedding_book = WeddingBook(config)
        wedding_book.gpio_setup()

        gpio_device = wedding_book.gpio_device
        
        # Initial state
        self.assertEqual(False, gpio_device.is_active)
        self.assertEqual(wedding_book.wbm.idling, wedding_book.wbm.current_state)
        sleep(1)
        # Pick up
        print("Pick up")
        gpio_pin.drive_low()
        self.assertEqual(True, gpio_device.is_active)
        self.assertEqual(wedding_book.wbm.playing, wedding_book.wbm.current_state)
        sleep(6)
        gpio_pin.drive_high()

    def test_aborting_the_playing_state(self):
        print("Test aborting the Playing-State")
        Device.pin_factory  = MockFactory()
        gpio_pin = Device.pin_factory.pin(17)
        config = { "gpio_index":17, "device_index": 1 }
        wedding_book = WeddingBook(config)
        wedding_book.gpio_setup()

        gpio_device = wedding_book.gpio_device
        
        # Initial state
        self.assertEqual(False, gpio_device.is_active)
        self.assertEqual(wedding_book.wbm.idling, wedding_book.wbm.current_state)
        sleep(1)
        # Pick up
        print("Pick up")
        gpio_pin.drive_low()
        self.assertEqual(True, gpio_device.is_active)
        self.assertEqual(wedding_book.wbm.playing, wedding_book.wbm.current_state)
        sleep(2)
        # Hang up
        print("Hang up")
        gpio_pin.drive_high()
        self.assertEqual(False, gpio_device.is_active)
        self.assertEqual(wedding_book.wbm.idling, wedding_book.wbm.current_state)


    def test_recording_and_hangup_after_4_seconds(self):
        print("Test REcording and hang up after 4 seconds")
        Device.pin_factory  = MockFactory()
        gpio_pin = Device.pin_factory.pin(17)
        config = { "gpio_index":17, "device_index": 1 }
        wedding_book = WeddingBook(config)
        wedding_book.gpio_setup()

        gpio_device = wedding_book.gpio_device
        
        # Initial state
        self.assertEqual(False, gpio_device.is_active)
        self.assertEqual(wedding_book.wbm.idling, wedding_book.wbm.current_state)
        sleep(1)
        # Pick up
        print("Pick up")
        gpio_pin.drive_low()
        self.assertEqual(True, gpio_device.is_active)
        self.assertEqual(wedding_book.wbm.playing, wedding_book.wbm.current_state)
        sleep(10)
        self.assertEqual(wedding_book.wbm.recording, wedding_book.wbm.current_state)
        # Hang up
        print("Hang up")
        gpio_pin.drive_high()
        self.assertEqual(False, gpio_device.is_active)
        self.assertEqual(wedding_book.wbm.idling, wedding_book.wbm.current_state)
        

if __name__ == '__main__':
    unittest.main()
