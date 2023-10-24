import pyaudio

class InputOutputSelector:

    def __init__(self, prefered_microphone_id=None, prefered_speaker_id=None):
        self.__microphone = None
        self.__speaker = None
        self.__py_audio = pyaudio.PyAudio()
        self.__microphones = {}
        self.__speakers = {}
        self.__unknown_devices = {}
        for ii in range(self.__py_audio.get_device_count()):
            device_info = self.__py_audio.get_device_info_by_index(ii)
            print(device_info)
        #     device_name = device_info.get('name')
        #     if 'Kopf' in device_name or 'mikro' in device_name:
        #         self.__microphones[ii] = device_name
        #     elif 'Lautsprecher' in device_name or 'Speaker' in device_name:
        #         self.__speakers[ii] = device_name
        #     else:
        #         self.__unknown_devices[ii] = device_name
        #     # print(p.get_device_info_by_index(ii).get('name'))
        # if prefered_microphone_id:
        #     self.__microphone = self.__microphones[prefered_microphone_id]
        # if prefered_speaker_id:
        #     self.__speaker = self.__speakers[prefered_speaker_id]
        # print(self.__microphones)
        # print(self.__speakers)
        # print(self.__unknown_devices)
        # print(self.__microphone)
        # print(self.__speaker)

InputOutputSelector(6, 15)
