# import RPi.GPIO as GPIO
# import time
# from time import sleep

class EventHandler:

    def __init__(self, state_machine):
        self.__state_machine = state_machine
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(2, GPIO.IN)


    def on_processing(self):
        while


    def pick_up(self):
        self.__state_machine.send('record')

    def hang_up(self):
        self.__self.__state_machine.send('idling')
