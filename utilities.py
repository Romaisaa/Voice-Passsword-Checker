from scipy import signal
import numpy as np
from scipy.io.wavfile import read
import librosa
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                    iterate_structure, binary_erosion)
from python_speech_features import mfcc

def replaceZeroes(data):
  min_nonzero = np.min(data[np.nonzero(data)])
  data[data < 0.0000001] = 0.0000001
  return data

def dataToDraw():
    audioData, sr = librosa.load("audio.wav")
    time, freq,nPxx,time_idx,freq_idx=spectro_plot(audioData,sr)
    time2, freq2,nPxx2= mfcc_plot(audioData, sr)

  
    return  time, freq,nPxx,time_idx,freq_idx, time2, freq2,nPxx2
  
def spectro_plot(audioData,sr):
    N = 256
    w = signal.blackman(N)
    nFreqs, nTime, nPxx = signal.spectrogram(audioData, window=w, nfft=N)
    nPxx=replaceZeroes(nPxx)
    nPxx=  10*np.log10(nPxx)
    # nPxx[nPxx < -100] =-60

    base=generate_binary_structure(2,1)
    structure=iterate_structure(generate_binary_structure(2,1),5)
    local_max=maximum_filter(nPxx, footprint=structure)==nPxx
    zeros= nPxx==0
    eroded_zeros= binary_erosion(zeros,structure=structure,border_value=1)
    peaks=local_max^eroded_zeros
    amps= nPxx[peaks]
    i,j =np.where(peaks)
    amps=amps.flatten()
    zipped_peaks=zip(j,i,amps)
    filter_peaks= filter(lambda x: x[2] > -10, zipped_peaks)
    filter_peaks=np.array(list(filter_peaks))
    try:
        time_idx=np.array(list(filter_peaks))[:,0]
        freq_idx=np.array(list(filter_peaks))[:,1]
    except:
        time_idx=np.array([])
        freq_idx=np.array([])
    time= np.linspace(0,nPxx.shape[0],nPxx.shape[0])
    freq= np.linspace(0,nPxx.shape[1],nPxx.shape[1])
    print(nPxx.shape)
    return  time.tolist(), freq.tolist(),nPxx.tolist(),time_idx.tolist(),freq_idx.tolist()

def mfcc_plot(audioData,sr):
    MFCC= librosa.feature.melspectrogram(y=audioData,sr=sr)
    time= np.linspace(0,MFCC.shape[0],MFCC.shape[0])
    freq= np.linspace(0,MFCC.shape[1],MFCC.shape[1])
    return  time.tolist(), freq.tolist(),MFCC.tolist()