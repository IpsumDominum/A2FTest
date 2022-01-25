import sys
import os
import vosk
import time
from utils import BASE_DIR
from recognizers.recognizer import Recognizer 
import cmudict
class Vosk_Recognizer(Recognizer):
    def __init__(self):
        super(Recognizer,self).__init__()
        model_path = os.path.join(BASE_DIR,"models","small-model")
        self.model = vosk.Model(model_path)
        self.rec = vosk.KaldiRecognizer(self.model,16000)
        self.start_time = 0
        self.word_read_num = 0
        self.clear = False        
        self.cmu_dict = cmudict.dict() 
    def audio_to_words(self,audio):        
        if self.rec.AcceptWaveform(audio):
            res = eval(self.rec.Result())["text"]
            self.clear = True
        else:
            res = eval(self.rec.PartialResult())["partial"]
        return res.split(" ")    
    def inference(self,audio_data):
        words = self.audio_to_words(audio_data)
        next_phonems = []
        next_tokens = []        
        for token_loc,token in enumerate(words):
            if(token_loc>=self.word_read_num and token!="" and len(self.cmu_dict[token])>0):
                self.word_read_num +=1
                next_phonems.append(self.cmu_dict[token][0])
                next_tokens.append(token)
                print(token)
                print(self.cmu_dict[token][0])
                print("="*20)
        aligned_phonems = self.align_phonem_to_audio_primitive(next_phonems,audio_data)
        if(self.clear==True):
            self.word_read_num = 0
            self.clear = False
        return aligned_phonems,next_tokens
