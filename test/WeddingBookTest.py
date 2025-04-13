import unittest
import WeddingBook
from unittest.mock import patch, MagicMock


class MyTestCase(unittest.TestCase):
    @patch('gpiozero.GPIODevice')
    def test_something(self, MockGPIODevice):
        wedding_book = WeddingBook.WeddingBook()
        # Setup des Mocks
        mock_instance = MockGPIODevice.return_value
        wedding_book.gpio_setup()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
