import numpy as np
import cv2
from utils import show_display
import threading
import os
from utils import BASE_DIR
class Animator():
    def __init__(self):
        def load_all_face_visemes():
            all_visemes = ['Rest', 'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', 'EH', 'ER', 'EY', 'F', 'G', 'HH', 'IH', 'IY', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH', 'UW', 'V', 'W', 'Y', 'Z', 'ZH']            
            visemes_images = {}
            for viseme in all_visemes:
                visemes_images[viseme] = cv2.imread(os.path.join(BASE_DIR,"Visemes",viseme+".png"))
            return visemes_images
        def load_all_visemes():            
            all_visemes = ["Ah","F V","R","B M P","Ih","S Z","Ch J","K G","T L D","Ee",
            "N Ng","Th","Er","Oh","W Oo"]
            all_images = cv2.imread(
                os.path.join(BASE_DIR,"Visemes","visemes.jpg")
                )
            width = 219
            height = 243
            print(all_images.shape)
            visemes_images = {}
            idx = 0
            for i in range(5):
                for j in range(3):
                    viseme = all_visemes[idx]
                    visemes_images[viseme] = all_images[j*height:(j+1)*height,i*width:(i+1)*width,:]
                    idx +=1
            return visemes_images
        self.mode = "Photo"
        if(self.mode=="Face"):
            self.visemes = load_all_face_visemes()
            self.idle_image = self.visemes["Rest"]
        else:
            self.visemes = load_all_visemes()
            self.idle_image = self.visemes["B M P"]
        self.animate_buffer = []
        self.phonem_input_buffer = []
        self.stopped = True
    def play_phonem_sequence(self,phonem_sequence):
        for phonem_item in phonem_sequence:
            if(self.mode!="Face"):
                viseme_code = self.phonem_to_viseme(phonem_item["phonem"])
            else:                
                viseme_code = phonem_item["phonem"]
                if(len(viseme_code)==3):
                    viseme_code = viseme_code[:2]
            split = viseme_code.split("|")
            for i in range(len(split)):
                self.animate_buffer.append(
                    (self.visemes[split[i]],int(phonem_item["duration"]/(i+1)))
                )
    def input_phonems(self,phonem_sequence):   
        if(len(phonem_sequence)>0):
            self.phonem_input_buffer.append(phonem_sequence)
    def render_animate_buffer(self):
        while(True):
            if(len(self.animate_buffer)>0):
                viseme_image,duration = self.animate_buffer.pop()
                k = show_display("Face",viseme_image,duration)
            else:
                k = show_display("Face",self.idle_image,1)
                break
        return k
    def run(self):
        def run_async():
            while(True):
                if(len(self.phonem_input_buffer)>0):
                    next_phonems = self.phonem_input_buffer.pop()
                    duration = self.play_phonem_sequence(next_phonems)
                self.render_animate_buffer()
                if(self.stopped):
                    break
        self.stopped = False
        animate_thread = threading.Thread(target=run_async)
        animate_thread.start()
    def stop(self):
        self.stopped = True        
        cv2.destroyAllWindows()
    def phonem_to_viseme(self,phonem):
        conversion_dict = {
            "AA":"Oh",
            "AE":"Ah", #AE T
            "AH":"Ah",
            "AO":"Oh|W Oo",
            "AW":"Ah|W Oo",#	cow	K AW
            "AY":"Ah|Ee",#	hide	HH AY D
            "B": "B M P", #be	B IY
            "CH": "Ch J",#cheese	CH IY Z
            "D" : "T L D",#	dee	D IY
            "DH": "Th",#	thee	DH IY
            "EH":"Ih",#	Ed	EH D
            "ER":"Er",#	hurt	HH ER T
            "EY":"Ih",#	ate	EY T
            "F":"F V",# 	fee	F IY
            "G":"K G",# 	green	G R IY N
            "HH":"Ih",#	he	HH IY
            "IH":"Ih",#	it	IH T
            "IY":"Ih|Ee",#	eat	IY T
            "JH":"K G",#	gee	JH IY
            "K":"K G",# 	key	K IY
            "L":"T L D",# 	lee	L IY
            "M":"B M P",# 	me	M IY
            "N":"N Ng|Ee",# 	knee	N IY
            "NG":"N Ng",#	ping	P IH NG
            "OW":"R|W Oo",#oat	OW T
            "OY":"W Oo|Ee",#	toy	T OY
            "P":"B M P|Ee",# 	pee	P IY
            "R":"Er|Ee",# 	read	R IY D
            "S":"S Z",# 	sea	S IY
            "SH":"Ch J",#	she	SH IY
            "T":"Th|Ee",# 	tea	T IY
            "TH":"Th",#	theta	TH EY T AH
            "UH":"W Oo",#	hood	HH UH D
            "UW":"W Oo",#	two	T UW
            "V":"F V|Ee",# 	vee	V IY
            "W":"W Oo|Ee",#	we	W IY
            "Y":"Ih",#yield	Y IY L D
            "Z":"S Z|Ee",# 	zee	Z IY
            "ZH":"S Z|Er"	#seizure	S IY ZH ER
        }
        if(len(phonem)==3):
            phonem = phonem[:2]
        if(phonem in conversion_dict.keys()):
            return conversion_dict[phonem]
        else:
            return conversion_dict["AA"]
        
     