from a2f.animators.default_animator import Animator
from a2f.phonem_recognizer import Phonem_Recognizer
import sounddevice as sd

rec = Phonem_Recognizer("vosk")
rec.recognize_from_microphone()

ani = Animator()
ani.run()

while(True):
    try:                
        aligned_phonems,next_tokens = rec.get_next()
        ani.input_phonems(aligned_phonems)
        if("exit" in next_tokens):
            break
    except KeyboardInterrupt:        
        break
ani.stop()
rec.stop()
