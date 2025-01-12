import pyaudio
import json
from webserver.settings import BASE_DIR
import os

class InputOutputSelector:

    CONFIG_PATH = os.path.join(BASE_DIR, 'webui/resources/config')

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
    
    def devices(self):
        py_audio = pyaudio.PyAudio()
        devices = []
        for id in range(py_audio.get_device_count()):
            device_info = py_audio.get_device_info_by_index(id)
            device_name = device_info.get('name')
            enabled = id==self.__prefered_device
            line = (enabled, id, device_name)
            devices.append(line)
        return devices

    def save(self, id):
        self.__prefered_device = id
        dictionary = {
            "dev_index": self.__prefered_device
        }
        if not os.path.exists(self.CONFIG_PATH):
            print(self.CONFIG_PATH)
            os.makedirs(self.CONFIG_PATH)
        # Serializing json
        json_object = json.dumps(dictionary, indent=1)
        # Writing to sample.json
        with open(f'{self.CONFIG_PATH}/config.json', 'w') as outfile:
            outfile.write(json_object)

    def load(self):
        with open(f'{self.CONFIG_PATH}/config.json', 'r') as openfile:
            json_object = json.load(openfile)
        self.__prefered_device = int(json_object["dev_index"])
        return self.__prefered_device