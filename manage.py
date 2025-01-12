#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from webui import WeddingBook


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver.settings')
    try:
        from django.core.management import execute_from_command_line
        #wb = WeddingBook.WeddingBook()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # try:
    #     setup_logging()
        
    #     # run_by = input("Run by: \n [1] Keyboard Input \n [2] Circuit Input \n Enter 1 or 2.")
    #     # if run_by == '1':
    #     #     wb.run_by_keyboard_input()
    #     # elif run_by == '2':
    #     wb.run_by_circuit_input()
    #     # else:
    #     #     print("No valid input. Program has been stopped!")


    # except KeyboardInterrupt:
    #     GPIO.cleanup()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
