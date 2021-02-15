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
    fe, data = wave_reading()
    n = data.size
    N = n
    t = 1.0 * n / fe
    te = 1.0 / fe
    t2 = np.arange(-n / 2, n / 2, 1)
    omega_b = (t2/N)*fe

    time = np.zeros(n)
    for k in range(n):
        time[k] = te*k

    #fentre de hanning pour la moustache
    #hanning = np.hanning(N)
    #data_hanning = data*hanning
    data_fft = np.fft.fft(data, N)
    data_fft_abs = np.abs(data_fft)

    # concaténation des data 0 à 80 k centré a 0
    FreqLog = 20 * np.log10(data_fft_abs[:80000])

    # 32 harmonique
    data_sin32,_ = signal.find_peaks(FreqLog, distance=1735, prominence= 17)

    data_amp = np.abs(FreqLog[data_sin32])

    sin = 0
    for x in range(0,32):
        sin += data_sin32[x]

    plt.figure()
    #plt.stem(np.abs())

    #filtre passe bas
    ohm_bar = np.pi / 1000

    # for N1 in range(1, 885):
    #     n1 = np.arange(0, N1-1, 1)
    #     passeBas = np.abs((1/N1)*np.sum(np.exp(-1j*(n1*ohm_bar))))
    #     print(N1, passeBas)

    N1 = 884  # trouver grace a la boucle for
    #n1 = np.arange(0, N1-1, 1)
    #passeBas = np.abs((1 / N1) * np.sum(np.exp(-1j * (n1 * ohm_bar))))
    hk = []

    for temp in range(0, N1):
        hk.append(1/N1)

    enveloppe = signal.fftconvolve(np.abs(data), hk)


    plt.figure()
    plt.plot(time, data)
    plt.ylabel('Amplitude')
    plt.xlabel('Temps (s)')
    plt.title('Spectre des amplitudes Fourier (LA#)')

    plt.figure()
    plt.plot(omega_b[80000:],FreqLog)
    plt.title('Sinusoidal principal')

    plt.figure()
    plt.plot(enveloppe)
    plt.title('Enveloppe filtré')

    plt.show()


if __name__ == "__main__":
    main()