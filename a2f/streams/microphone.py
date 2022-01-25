import sounddevice as sd
import sys
import queue
class Microphone():
    def __init__(self,sample_rate=16000,device=-1):
        def store_audio_in_buffer(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)            
            self.queue.put(bytes(indata))
        self.device = self.find_input_device() if(device==-1) else device
        self.queue = queue.Queue()
        self.stream = sd.RawInputStream(samplerate=sample_rate, blocksize = 5000, device=self.device, dtype='int16',
                                channels=1, callback=store_audio_in_buffer)
    def find_input_device(self):
        device_index = -1
        for device_index,device in enumerate(sd.query_devices()):
            device_name = device['name']
            for keyword in ['mic','input']:
                if keyword in device_name.lower():
                    print('Found a device: device {} - {}'.format(device_index,device_name))
                    return device_index
        if(device_index==-1):
            print("Error::Cannot automatically find device, please specify device from following list:")
            print(sd.query_devices())
            exit()
    def next_data(self):
        return self.queue.get()