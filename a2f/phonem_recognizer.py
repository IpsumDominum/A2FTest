from recognizers.vosk_recognizer import Vosk_Recognizer
from recognizers.stt_recognizer import STT_Recognizer
from streams.microphone import Microphone
import queue
import threading
class Phonem_Recognizer():
    def __init__(self,model_name):
        if(model_name=="vosk"):
            self.model = Vosk_Recognizer()
        else:
            self.model = STT_Recognizer()        
        self.buffer = queue.Queue()
        self.stopped = False
    def recognize_from_microphone(self):
        def main_loop():
            mic = Microphone()
            with mic.stream:
                while (True):
                    audio_data = mic.next_data()
                    result = self.model.inference(audio_data)
                    self.buffer.put(
                        result
                        )
                    if(self.stopped==True):
                        break
        self.stopped = False
        thread = threading.Thread(target=main_loop)
        thread.start()
    def get_next(self):
        return self.buffer.get()
    def stop(self):
        self.stopped = True
