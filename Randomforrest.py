import librosa
import os
import numpy as np
import scipy
import pandas as pd
import pickle
def power_to_db(S, ref=1.0, amin=1e-10, top_db=80.0):
    S = np.asarray(S)
    magnitude = S
    ref_value = np.abs(1.0)
    log_spec = 10.0 * np.log10(np.maximum(1e-10, magnitude))
    log_spec -= 10.0 * np.log10(np.maximum(1e-10, ref_value))
    log_spec = np.maximum(log_spec, log_spec.max() - top_db)
    return log_spec


def expand_to(x, ndim, axes):
    # Force axes into a tuple
    try:
        axes = tuple(axes)
    except TypeError:
        axes = tuple([axes])

    shape = [1] * ndim
    for i, axi in enumerate(axes):
        shape[axi] = x.shape[i]

    return x.reshape(shape)

def mfcc(y=None, sr=22050, S=None, n_mfcc=20, dct_type=2, norm="ortho", lifter=0, **kwargs):
    if S is None:
        # multichannel behavior may be different due to relative noise floor differences between channels
        S = power_to_db(melspectrogram(y=y, sr=sr, **kwargs))

    M = scipy.fftpack.dct(S, axis=-2, type=dct_type, norm=norm)[..., :n_mfcc, :]

    if lifter > 0:
        # shape lifter for broadcasting
        LI = np.sin(np.pi * np.arange(1, 1 + n_mfcc, dtype=M.dtype) / lifter)
        LI = expand_to(LI, ndim=S.ndim, axes=-2)

        M *= 1 + (lifter / 2) * LI
        return M
    elif lifter == 0:
        return M

def melspectrogram(y=None, sr=22050, S=None, n_fft=2048, hop_length=512, win_length=None, window="hann", center=True,
                   pad_mode="constant", power=2.0, **kwargs):

    S, n_fft = _spectrogram(y=y, S=S, n_fft=n_fft, hop_length=hop_length, power=power, win_length=win_length, window=window,
                            center=center,pad_mode=pad_mode,)

    # Build a Mel filter
    mel_basis = mel(sr=sr, n_fft=n_fft, **kwargs)

    return np.einsum("...ft,mf->...mt", S, mel_basis, optimize=True)

def _spectrogram(y=None, S=None, n_fft=2048, hop_length=512, power=1, win_length=None, window="hann", center=True,
                 pad_mode="constant"):

    if S is not None:
        # Infer n_fft from spectrogram shape, but only if it mismatches
        if n_fft // 2 + 1 != S.shape[-2]:
            n_fft = 2 * (S.shape[-2] - 1)
    else:
        # Otherwise, compute a magnitude spectrogram from input
        S = (
            np.abs(
                librosa.stft(
                    y,
                    n_fft=n_fft,
                    hop_length=hop_length,
                    win_length=win_length,
                    center=center,
                    window=window,
                    pad_mode=pad_mode,
                )
            )
            ** power
        )

    return S, n_fft

def fft_frequencies(sr=22050, n_fft=2048):
    return np.fft.rfftfreq(n=n_fft, d=1.0 / sr)
def mel(sr, n_fft, n_mels=128, fmin=0.0, fmax=None, htk=False, norm="slaney", dtype=np.float32):
    if fmax is None:
        fmax = float(sr) / 2

    # Initialize the weights
    n_mels = int(n_mels)
    weights = np.zeros((n_mels, int(1 + n_fft // 2)), dtype=dtype)

    # Center freqs of each FFT bin
    fftfreqs = fft_frequencies(sr=sr, n_fft=n_fft)

    # 'Center freqs' of mel bands - uniformly spaced between limits
    mel_f = mel_frequencies(n_mels + 2, fmin=fmin, fmax=fmax, htk=htk)

    fdiff = np.diff(mel_f)
    ramps = np.subtract.outer(mel_f, fftfreqs)

    for i in range(n_mels):
        # lower and upper slopes for all bins
        lower = -ramps[i] / fdiff[i]
        upper = ramps[i + 2] / fdiff[i + 1]

        # .. then intersect them with each other and zero
        weights[i] = np.maximum(0, np.minimum(lower, upper))

    if norm == "slaney":
        # Slaney-style mel is scaled to be approx constant energy per channel
        enorm = 2.0 / (mel_f[2 : n_mels + 2] - mel_f[:n_mels])
        weights *= enorm[:, np.newaxis]
    else:
        weights = normalize(weights, norm=norm, axis=-1)

    return weights

def mel_frequencies(n_mels=128, fmin=0.0, fmax=11025.0, htk=False):
    # 'Center freqs' of mel bands - uniformly spaced between limits
    min_mel = hz_to_mel(fmin, htk=htk)
    max_mel = hz_to_mel(fmax, htk=htk)

    mels = np.linspace(min_mel, max_mel, n_mels)

    return mel_to_hz(mels, htk=htk)

def hz_to_mel(frequencies, htk=False):
    frequencies = np.asanyarray(frequencies)

    if htk:
        return 2595.0 * np.log10(1.0 + frequencies / 700.0)

    # Fill in the linear part
    f_min = 0.0
    f_sp = 200.0 / 3

    mels = (frequencies - f_min) / f_sp

    # Fill in the log-scale part

    min_log_hz = 1000.0  # beginning of log region (Hz)
    min_log_mel = (min_log_hz - f_min) / f_sp  # same (Mels)
    logstep = np.log(6.4) / 27.0  # step size for log region

    if frequencies.ndim:
        # If we have array data, vectorize
        log_t = frequencies >= min_log_hz
        mels[log_t] = min_log_mel + np.log(frequencies[log_t] / min_log_hz) / logstep
    elif frequencies >= min_log_hz:
        # If we have scalar data, heck directly
        mels = min_log_mel + np.log(frequencies / min_log_hz) / logstep

    return mels

def mel_to_hz(mels, htk=False):
    mels = np.asanyarray(mels)

    if htk:
        return 700.0 * (10.0 ** (mels / 2595.0) - 1.0)

    # Fill in the linear scale
    f_min = 0.0
    f_sp = 200.0 / 3
    freqs = f_min + f_sp * mels

    # And now the nonlinear scale
    min_log_hz = 1000.0  # beginning of log region (Hz)
    min_log_mel = (min_log_hz - f_min) / f_sp  # same (Mels)
    logstep = np.log(6.4) / 27.0  # step size for log region

    if mels.ndim:
        # If we have vector data, vectorize
        log_t = mels >= min_log_mel
        freqs[log_t] = min_log_hz * np.exp(logstep * (mels[log_t] - min_log_mel))
    elif mels >= min_log_mel:
        # If we have scalar data, check directly
        freqs = min_log_hz * np.exp(logstep * (mels - min_log_mel))

    return freqs

def normalize(S,norm=np.inf, axis=0):
    threshold = np.finfo(np.float32).tiny

    mag = np.abs(S).astype(float)
    fill_norm = 1
    length = np.sum(mag**norm, axis=axis, keepdims=True) ** (1.0 / norm)
    fill_norm = mag.shape[axis] ** (-1.0 / norm)
    small_idx = length < threshold
    Snorm = np.empty_like(S)
    length[small_idx] = 1.0
    Snorm[:] = S / length

    return Snorm

def extract_features(file):
    global name
        # Loads the audio file as a floating point time series and assigns the default sample rate
        # Sample rate is set to 22050 by default
    X, sample_rate = librosa.load(file["file"], res_type='kaiser_fast')
        
        # Generate Mel-frequency cepstral coefficients (MFCCs) from a time series 
    mfccs = np.mean(mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)

        # Generates a Short-time Fourier transform (STFT) to use in the chroma_stft
    stft = np.abs(librosa.stft(X))

        # Computes a chromagram from a waveform or power spectrogram.
    chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)

        # Computes a mel-scaled spectrogram.
    mel = np.mean(melspectrogram(X, sr=sample_rate).T,axis=0)

        # Computes spectral contrast
    contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)

        # Computes the tonal centroid features (tonnetz)
    tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)


    return mfccs, chroma, mel, contrast, tonnetz

def feat(features_label):
    features = []
    for i in range(0, len(features_label)):
        features.append(np.concatenate((features_label[i][0], features_label[i][1], 
                features_label[i][2], features_label[i][3],
                features_label[i][4]), axis=0))
    return features    

def predict_voice():
    clf = pickle.load(open('speaker-model.pkl', 'rb'))
    df_test= pd.DataFrame(["audio.wav"], columns=["file"])
    df_test=df_test.apply(extract_features,axis=1)
    df_test= feat(df_test)
    return clf.predict(df_test)
