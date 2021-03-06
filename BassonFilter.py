import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wave
from scipy import signal

import FileManager as fileManager


def time(teBasson, nBasson):
    time = np.zeros((nBasson))
    for k in range(nBasson):
        time[k] = teBasson * k
    return time


def fft(dataBasson, nBasson):
    han = np.hanning(nBasson)
    fft = han*dataBasson
    fft = np.fft.fft(fft, nBasson)
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


def filtrageBasson(graphicsOn=False):
    # lecture du fichier .wav d'origine
    rateBasson, dataBasson = fileManager.waveRead('note_basson_plus_sinus_1000_Hz.wav')
    rateNewBasson, dataNewBasson = fileManager.waveRead('bassonFiltre.wav', "out")

    # initialisation des variable
    N = 6000
    fe = rateBasson
    nBasson = dataBasson.size
    nNewBasson = dataNewBasson.size
    w0 = 2*np.pi*1000/rateBasson
    w1 = 2*np.pi*40/rateBasson

    f = (w1 / (2 * np.pi)) * fe
    K = (f / fe) * N * 2 + 1

    n = np.arange((-N / 2) + 1, (N / 2) + 1, 1)

    teBasson = 1.0 / rateBasson
    teNewBasson = 1.0 / rateNewBasson
    tBasson = np.arange(-nBasson / 2, nBasson / 2, 1)
    omega_b_Basson = (tBasson / nBasson) * rateBasson

    timeBasson = time(teBasson, nBasson)

    timeNewBasson = time(teNewBasson, nNewBasson)

    Bassonfft = fft(dataBasson, nBasson)

    # Frequence en log des data 0 à 67525
    FreqLog = 20 * np.log10(Bassonfft[:67525])

    N1 = 884
    hk = []

    for temp in range(0, N1):
        hk.append(1 / N1)

    # passe bas
    h_n = (1 / N) * (np.sin(np.pi * n * K / N) / (np.sin(np.pi * n / N)))
    h_n[int(N / 2 - 1)] = K / N

    # coupe bande
    delta_n = np.zeros(N)
    delta_n[int(N / 2)] = 1
    yn = delta_n - (2 * h_n * np.cos(w0 * n))

    # convolution entre data et le coupe bande
    basson = np.convolve(dataBasson, yn)

    for x in range(0, 2):
        basson = np.convolve(basson, yn)

    enveloppe = signal.fftconvolve(np.abs(dataBasson), hk)

    # ecriture dans le fichier .wav
    # wave_writing(rateBasson, basson)
    fileManager.waveWrite("newBasson.wav", rateBasson, basson)


    #  Reponse impulsionnel
    cb1, cb_1 = signal.freqz(yn)

    if graphicsOn:
        affichage('Spectre des amplitudes Fourier (Basson non filtré)', 'Temps (s)', 'Amplitude', timeBasson, dataBasson)
        affichage('Peaks (sinus principal) non filtré Basson', 'Fréquences (Hz)', 'Amplitude (db)', omega_b_Basson[67526:], FreqLog)
        affichage1('Enveloppe filtré Basson', 'Nombre d''échantillon', 'Amplitude', enveloppe)
        affichage('Spectre des amplitudes Fourier (Basson filtré)', 'Temps (s)', 'Amplitude', timeNewBasson, basson)

        affichage('Réponse impulsionnel du filtre coupe bande (h[n])', 'Nombre d''échantillon ', 'Amplitude', n, h_n)

        plt.figure()
        plt.plot(timeBasson, dataBasson, 'b', label='Signal original')
        plt.plot(timeNewBasson, basson, 'r', label='Signal filtré')
        plt.legend()
        plt.ylabel('Amplitude')
        plt.xlabel('Temps (s)')
        plt.title('Spectre des amplitudes Fourier Basson')

        plt.figure()
        plt.plot(timeBasson[:1750], dataBasson[:1750], 'b', label='Signal original')
        plt.plot(timeNewBasson[:1750], basson[:1750], 'r', label='Signal filtré')
        plt.legend()
        plt.ylabel('Amplitude')
        plt.xlabel('Temps (s)')
        plt.title('Réponse du sinus de 1000Hz dans le filtre coupe bande')

        fig, ax1 = plt.subplots()
        ax1.set_title('Réponse en fréquence du coupe bande du basson')
        ax1.plot(cb1, 20 * np.log10(abs(cb_1)), 'b')
        ax1.set_ylabel('Amplitude [dB]', color='b')
        ax1.set_xlabel('Fréquences (rad/échantillon)')

        ax2 = ax1.twinx()
        angles = np.unwrap(np.angle(cb_1))
        ax2.plot(cb1, angles, 'g')
        ax2.set_ylabel('Angle (radians)', color='g')
        ax2.grid()

        plt.show()
