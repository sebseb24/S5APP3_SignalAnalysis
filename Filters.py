import sys
import math
from math import sin, pi
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wave
from scipy import signal


def wave_reading():
    fe, data = wave.read('note_guitare_LAd.wav')
    return fe, data


def main():
    f = 466
    fe, data = wave_reading()
    data = np.array(data)
    n = data.size
    N = n
    t = 1.0 * n / fe
    te = 1.0 / fe
    xm = []

    time = np.zeros(n)
    for k in range (n):
        time[k] = te*k

    #eveloppe avec hilbert
    data_env = signal.hilbert(data)
    data_abs = np.abs(data_env)

    #fentre de hanning pour la moustache
    hanning = np.hanning(N)
    data_hanning = data*hanning
    data_fft = np.fft.fft(data_hanning, N)
    data_fft_abs = np.abs(data_fft)

    # omega _ pour l'Axe en frequence normalisé
    t1 = np.arange(0.0, n, 1)
    # boucle pour le omega (axe x) pour b)
    for x in t1:
        xm.append(2 * np.pi * x / fe)

    # concaténation des data -80k à 80 k centré a 0
    t2 = np.arange(-n / 2, n / 2, 1)
    FreqLog = 20 * np.log10(data_fft_abs)
    flipData = np.concatenate((FreqLog[80000:], FreqLog[:80000]))



    plt.figure()
    plt.plot(time, data)
    plt.ylabel('Amplitude')
    plt.xlabel('Temps (s)')
    plt.title('Spectre des amplitudes Fourier (LA#)')

    plt.figure()
    plt.plot(t2, flipData)
    plt.title('TFD(LA#) Fenetre Hanning')

    plt.figure()
    plt.plot(xm, data_abs)
    plt.title('Enveloppe')

    plt.show()

    print(n)
    print(t)
    print(te)
    print(fe)
    print(time)


if __name__ == "__main__":
    main()