import cmudict 
class Recognizer():
    def __init__(self):
        pass
    def align_phonem_to_audio_primitive(self,next_phonems,audio_data):
        aligned_phonems = []
        for phonem_sequence in next_phonems:
            for phonem in phonem_sequence:    
                aligned_phonems.append(
                    {"phonem":phonem,"duration":max(20,100-len(next_phonems)*10)}
                )
        return aligned_phonems