import pyaudio
import json
import os

class InputOutputSelector:

    config_path = 'resources/config'

    def __init__(self):
        self.__prefered_device = None

    def select_device(self):
        py_audio = pyaudio.PyAudio()
        for ii in range(py_audio.get_device_count()):
            device_info = py_audio.get_device_info_by_index(ii)
            device_name = device_info.get('name')
            print(f"ID: {ii} - Name: {device_name}")
        self.__prefered_device = int(input())
        return self

    def save(self):
        dictionary = {
            "dev_index": self.__prefered_device
        }
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)
        # Serializing json
        json_object = json.dumps(dictionary, indent=1)

        # Writing to sample.json
        with open(f'{self.config_path}/config.json', 'w') as outfile:
            outfile.write(json_object)

    def load(self):
        with open(f'{self.config_path}/config.json', 'r') as openfile:
            json_object = json.load(openfile)
        return int(json_object["dev_index"])