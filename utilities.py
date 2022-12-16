import numpy as np
import librosa
import pickle
from sklearn.decomposition import PCA

def dataToDraw():
    audioData, sr = librosa.load("audio.wav")
    time, freq,amp= mfcc_plot(audioData, sr)
    labels, mfcc, mfcc_coef= mfcc_coef_bar( audioData, sr)
    return  labels, mfcc,mfcc_coef,time, freq,amp
  


def mfcc_plot(audioData,sr):
    mel = librosa.feature.melspectrogram(audioData, sr=sr)
    mel_DB = librosa.power_to_db(mel, ref=np.max)
    time= np.linspace(0,mel_DB.shape[0],mel_DB.shape[0])
    freq= np.linspace(0,mel_DB.shape[0],mel_DB.shape[0])
    return  time.tolist(),freq.tolist(),mel_DB.tolist()

def mfcc_coef_bar(audioData,sr):
    mfcc= librosa.feature.mfcc(audioData,sr,n_mfcc=40)
    mfcc_means= np.mean(mfcc,axis=1)
    labels= [f"mfcc_{i+1}" for i in range(18)]
    pca=pickle.load(open("pca.pkl",'rb'))
    indies= [1013, 2721, 2722, 3071, 3072]
    data=mfcc.reshape(-1)[indies]


    return labels, mfcc_means[2:21].tolist(), data.tolist()