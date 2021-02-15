import sys
import math
from math import sin, pi
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wave
from scipy import signal


def newNote(freq, amp, rate, phase, tailles):
    taille = np.arange(tailles, dtype = float)/rate
    note = amp*np.sin(2*np.pi*freq*taille+phase)
    return note

def wave_reading():
    fe, data = wave.read('note_guitare_LAd.wav')
    return fe, data

def wave_write(name, rate, note):
    scaled = np.int16(note / np.max(np.abs(note)) * 32767)
    wave.write('lad.wav', rate, scaled)

def main():
    fe, data = wave_reading()
    n = data.size
    N = n
    t = 1.0 * n / fe
    te = 1.0 / fe
    t2 = np.arange(-n / 2, n / 2, 1)
    t3 = np.arange(0, n, 1, dtype=float)
    omega_b = (t2/N)*fe

    Freq_amp = []
    Freq_phase = []
    Freq_Harm = []

    time = np.zeros(n)
    for k in range(n):
        time[k] = te*k

    #fentre de hanning pour la moustache
    #hanning = np.hanning(N)
    #data_hanning = data*hanning
    data_fft = np.fft.fft(data, N)
    data_fft_abs = np.abs(data_fft)
    data_fft_ang = np.angle(data_fft)

    # concaténation des data 0 à 80 k centré a 0
    FreqLog = 20 * np.log10(data_fft_abs[:80000])

    # filtre passe bas
    #ohm_bar = np.pi / 1000
    # for N1 in range(1, 885):
    #     n1 = np.arange(0, N1-1, 1)
    #     passeBas = np.abs((1/N1)*np.sum(np.exp(-1j*(n1*ohm_bar))))
    #     print(N1, passeBas)

    N1 = 884  # trouver grace a la boucle for
    # n1 = np.arange(0, N1-1, 1)
    # passeBas = np.abs((1 / N1) * np.sum(np.exp(-1j * (n1 * ohm_bar))))
    hk = []

    for temp in range(0, N1):
        hk.append(1 / N1)

    enveloppe = signal.fftconvolve(np.abs(data), hk)

    # 32 harmonique
    data_sin32,_ = signal.find_peaks(FreqLog, distance=1735, prominence= 17)

    data_amp = np.abs(FreqLog[data_sin32])

    sin = 0
    for x in range(0,32):
        sin += data_sin32[x]

    axeFreq = (t3 * fe) / N

    for y in data_sin32:
        Freq_amp.append(data_fft_abs[y])
        Freq_phase.append(data_fft_ang[y])
        Freq_Harm.append(axeFreq[y])

    Freq0 = axeFreq[data_sin32[0]]
    #LaD = 1*Freq_Harm
    Sol = np.power(2.0, -3.0 / 12) * Freq_Harm

    SolHarm = []
    SolPhase = []
    SolAmp = []
    for z in Freq_Harm:
        SolHarm.append()



    newSin = np.zeros(len(enveloppe))
    for z in range(0, 32):
        newSin += newNote(Sol[y], Freq_amp[y], enveloppe.size, Freq_phase[y])

    LAD = newSin * enveloppe


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