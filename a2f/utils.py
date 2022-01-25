import subprocess
import numpy as np
import os
import cv2
try:
    from shlex import quote
except ImportError:
    from pipes import quote
import time
import matplotlib.pyplot as plt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def convert_samplerate(audio, desired_sample_rate):
    audio_path = "temp.wav"
    with open("temp.wav","wb") as file:
        file.write(audio)
    sox_cmd = "sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little --compression 0.0 --no-dither - ".format(
        quote(audio_path), desired_sample_rate
    )    
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("SoX returned non-zero status: {}".format(e.stderr))
    except OSError as e:
        raise OSError(
            e.errno,
            "SoX not found, use {}hz files or install it: {}".format(
                desired_sample_rate, e.strerror
            ),
        )
    if(os.isfile("temp.wav")):
        os.remove("temp.wav")
    return desired_sample_rate, np.frombuffer(output, np.int16)

def plot_show(audio_data):
    #plt.ylabel('Frequency [Hz]')
    #plt.xlabel('Time [sec]')
    # Make a random plot...
    fig = plt.figure()
    fig.add_subplot(111)
    plt.plot(audio_data)
    fig.canvas.draw()
    # Now we can save it to a numpy array.
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data

def TopK(x, k):
    if(len(x)<=k):
        return range(k),x
    a = dict([(i, j) for i, j in enumerate(x)])
    sorted_a = dict(sorted(a.items(), key = lambda kv:kv[1], reverse=True))
    indices = list(sorted_a.keys())[:k]
    values = list(sorted_a.values())[:k]
    return indices,values
def moving_average(a,n):    
    res = np.zeros((len(a),1))
    for i in range(len(a)):
        res[i] = np.mean(a[max(0,i-n//2):min(len(a),i+n//2)])
    return res
def plot_mfcc(audio_data,peak_num):
    #fbank_feat = ssc(audio_data,args.samplerate)
    fbank_feat = audio_data.reshape(audio_data.shape[0],1)
    fig = plt.figure()
    fig.add_subplot(111)
    #fbank_data = np.swapaxes(fbank_feat, 0 ,1)
    #cax = plt.imshow(fbank_data, interpolation='nearest', cmap=cm.inferno, origin='lower', aspect='auto')
    #fbank_feat = np.average(fbank_feat,axis=1)
    fbank_feat[fbank_feat<np.std(fbank_feat)] = 0
    plt.plot(fbank_feat)
    
    fbank_feat = moving_average(fbank_feat,10)
    indices,values = TopK(fbank_feat,peak_num)
    plt.plot(fbank_feat)
    for idx,v in zip(indices,values):
        plt.plot(idx, v, color='green', marker='o', linestyle='dashed',
                linewidth=2, markersize=5)
    fig.canvas.draw()
    # Now we can save it to a numpy array.
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data
def show_display(window_name,display_image,duration):
    cv2.imshow(window_name,display_image)
    k = cv2.waitKey(duration)
    return k

    
