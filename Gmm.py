import os
import wave
import time
import pickle
import numpy as np
from sklearn import preprocessing
from scipy.io.wavfile import read
import python_speech_features as mfcc
from sklearn.mixture import GaussianMixture
import librosa


def calculate_delta(array,n_mfcc):
   
    rows,cols = array.shape
    deltas = np.zeros((rows,n_mfcc))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
              first =0
            else:
              first = i-j
            if i+j > rows-1:
                second = rows-1
            else:
                second = i+j 
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas

def extract_features(audio,rate,mode):
    options={
        "Voice":{
            "winlen":0.025,
            "winstep":0.01,
            "nfft":1200,
            "n_mfcc":20
        },
        "Voc":{
            "winlen":0.1,
            "winstep":0.03,
            "nfft":2250,
            "n_mfcc":13
        }
    }
    mfcc_feature = mfcc.mfcc(audio,rate, options[mode]["winlen"],options[mode]["winstep"],options[mode]["n_mfcc"],nfft = options[mode]["nfft"], appendEnergy = True)    
    mfcc_feature = preprocessing.scale(mfcc_feature)
    delta = calculate_delta(mfcc_feature,options[mode]["n_mfcc"])
    combined = np.hstack((mfcc_feature,delta)) 
    return combined

def predict(mode):
    modelpath={
        "Voice":"models",
        "Voc":"models_voc"
    }
    
    gmm_files = [os.path.join(modelpath[mode],fname) for fname in
                  os.listdir(modelpath[mode]) if fname.endswith('.gmm')]
     
    #Load the Gaussian gender Models
    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
     
    # Read the test directory and get the list of test audio files 
    audio,sr = librosa.load("audio.wav")
    vector   = extract_features(audio,sr,mode)
        
    log_likelihood = np.zeros(len(models)) 
    
    for i in range(len(models)):
        gmm    = models[i]  #checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
         
    return log_likelihood