import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wave
from scipy import signal

def wave_reading(name):
    rate, data = wave.read(name)
    return rate, data

def wave_writing(rate, basson):
    wave.write('newBasson.wav', rate, basson.astype(np.int16))

def time(teBasson, nBasson):
    time = np.zeros((nBasson))
    for k in range(nBasson):
        time[k] = teBasson*k
    return time

def fft(dataBasson, nBasson):
    fft = np.fft.fft(dataBasson, nBasson)
    fft = np.abs(fft)
    return fft

def affichage(title, xlabel, ylabel, data1, data2):
    plt.figure()
    plt.plot(data1, data2)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)

def affichage1(title, xlabel, ylabel, data1):
    plt.figure()
    plt.plot(data1)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)

def main():
    #lecture du fichier .wav d'origine
    rateBasson, dataBasson = wave_reading('note_basson_plus_sinus_1000_Hz.wav')
    rateNewBasson, dataNewBasson = wave_reading('newBasson.wav')

    # initialisation des variable
    N = 6000
    fe = N
    nBasson = dataBasson.size
    nNewBasson = dataNewBasson.size
    w0 = 2*np.pi*960/6000
    w1 = 2*np.pi*1040/6000

    f = (w1/(2*np.pi))*fe
    K = (f/fe)*N*2+1

    n = np.arange((-N / 2)+1, (N / 2)+1, 1)

    teBasson = 1.0 / rateBasson
    teNewBasson = 1.0 / rateNewBasson
    tBasson = np.arange(-nBasson / 2, nBasson / 2, 1)
    tNewBasson = np.arange(-nNewBasson / 2, nNewBasson / 2, 1)
    omega_b_Basson = (tBasson / nBasson) * rateBasson
    omega_b_NewBasson = (tNewBasson / nNewBasson) * rateNewBasson

    timeBasson = time(teBasson, nBasson)

    timeNewBasson = time(teNewBasson, nNewBasson)

    Bassonfft = fft(dataBasson, nBasson)

    # Frequence en log des data 0 à 67525
    FreqLog = 20 * np.log10(Bassonfft[:67525])

    N1 = 884
    hk = []

    for temp in range(0, N1):
        hk.append(1 / N1)

    #passe bas
    h_n = (1 / N) * (np.sin(np.pi * n * K / N) / (np.sin(np.pi * n / N)))
    h_n[int(N/2-1)] = K / N


    #coupe bande
    delta_n = np.zeros(N)
    delta_n[int(N/2)] = 1
    yn = delta_n - (2 * h_n * np.cos(w0*n))

    #convolution entre data et le coupe bande
    basson = np.convolve(dataBasson, yn)

    for x in range(0,2):
        basson = np.convolve(basson,yn)


    enveloppe = signal.fftconvolve(np.abs(dataBasson), hk)

    # ecriture dans le fichier .wav
    wave_writing(rateBasson, basson)

    NewBassonfft = fft(basson, nNewBasson)

    # # Frequence en log des data 0 à 76524
    FreqLog1 = 20 * np.log10(NewBassonfft[:76524])

    affichage('Spectre des amplitudes Fourier (Basson non filtré)', 'Temps (s)', 'Amplitude', timeBasson, dataBasson)
    affichage('Peaks (sinus principal) non filtré', 'Fréquences (Hz)', 'Amplitude (db)', omega_b_Basson[67526:], FreqLog)
    affichage1('Enveloppe filtré', 'Nombre d''échantillon', 'Amplitude', enveloppe)
    affichage1('Filtre coupe-bande réponse en fréquence', 'Nombre d''échantillon', 'Amplitude', hk) # ajout de la phase
    affichage('Spectre des amplitudes Fourier (Basson filtré)', 'Temps (s)', 'Amplitude', timeNewBasson, basson) # faire la moustache synthétise
    affichage('Peaks (sinus principal) filtré', 'Fréquences (Hz)', 'Amplitude (db)', omega_b_NewBasson[76524:],FreqLog1)

    #tracer reponse impulsionnel
    #tracer reponse sin 100-Hz

    plt.show()

if __name__ == '__main__':
    main()