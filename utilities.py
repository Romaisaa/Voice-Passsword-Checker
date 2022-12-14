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
    time, freq,nPxx=spectro_plot(audioData,sr)
    time2, freq2,nPxx2= mfcc_plot(audioData, sr,freq)
    labels, mfcc= mfcc_coef_bar( audioData, sr)

  
    return  labels, mfcc,time2, freq2,nPxx2
  
def spectro_plot(audioData,sr):
    N = 256
    w = signal.blackman(N)
    nFreqs, nTime, nPxx = signal.spectrogram(audioData, window=w, nfft=N)
    nPxx=replaceZeroes(nPxx)
    nPxx=  10*np.log10(nPxx)
    return  nTime.tolist(), nFreqs.tolist(),nPxx.tolist()

def mfcc_plot(audioData,sr,time):
    S = librosa.feature.melspectrogram(audioData, sr=sr)
    S_DB = librosa.power_to_db(S, ref=np.max)
    time= np.linspace(0,S_DB.shape[0],S_DB.shape[0])
    freq= np.linspace(0,S_DB.shape[0],S_DB.shape[0])
    return  time.tolist(),freq.tolist(),S_DB.tolist()

def mfcc_coef_bar(audioData,sr):
    mfcc= librosa.feature.mfcc(audioData,sr)
    mfcc= np.mean(mfcc,axis=1)
    labels= [f"mfcc_{i+1}" for i in range(18)]

    return labels, mfcc[2:].tolist()