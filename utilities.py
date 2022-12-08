from scipy import signal
import numpy as np
from scipy.io.wavfile import read
import librosa

def replaceZeroes(data):
  min_nonzero = np.min(data[np.nonzero(data)])
  data[data == 0] = min_nonzero
  return data

def dataToDraw():
    audio_data,sample_freq= librosa.load("audio.wav")
    N = 512
    w = signal.blackman(N)
    nFreqs, nTime, nPxx = signal.spectrogram(audio_data, sample_freq, window=w, nfft=N)   
    print(nPxx)
    nPxx=replaceZeroes(nPxx)
    nPxx=  10*np.log10(nPxx)
    return  nTime.tolist(), nFreqs.tolist(),nPxx.tolist()
  