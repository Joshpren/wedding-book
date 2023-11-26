import pyaudio
import json

class InputOutputSelector:

    config_path = 'resources/config/config.json'

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
        # Serializing json
        json_object = json.dumps(dictionary, indent=1)

        # Writing to sample.json
        with open(self.config_path, 'w') as outfile:
            outfile.write(json_object)

    def load(self):
        with open(self.config_path, 'r') as openfile:
            json_object = json.load(openfile)
        return int(json_object["dev_index"])