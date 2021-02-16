import sys
import math
from math import sin, pi
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wave
from scipy import signal


def newNote(freq, amp, rate, phase, tailles):
    taille = np.arange(tailles, dtype=float) / rate
    note = amp * np.sin(2 * np.pi * freq * taille + phase)
    return note


def wave_reading():
    fe, data = wave.read('Sounds/note_guitare_LAd.wav')
    return fe, data


def wave_write(name, rate, note):
    scaled = np.int16(note / np.max(np.abs(note)) * 32767)
    wave.write(name, rate, scaled)


def main():
    fe, data = wave_reading()
    n = data.size
    N = n
    t = 1.0 * n / fe
    te = 1.0 / fe
    t2 = np.arange(-n / 2, n / 2, 1)
    t3 = np.arange(0, n, 1, dtype=float)
    omega_b = (t2 / N) * fe

    Freq_amp = []
    Freq_phase = []
    Freq_Harm = []

    time = np.zeros(n)
    for k in range(n):
        time[k] = te * k

    # fenetre de hanning pour la moustache
    # hanning = np.hanning(N)
    # data_hanning = data*hanning
    data_fft = np.fft.fft(data, N)
    data_fft_abs = np.abs(data_fft)
    data_fft_ang = np.angle(data_fft)

    # concaténation des data 0 à 80 k centré a 0
    FreqLog = 20 * np.log10(data_fft_abs[:80000])

    # filtre passe bas
    # ohm_bar = np.pi / 1000
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
    data_sin32, _ = signal.find_peaks(FreqLog, distance=1735, prominence=17)

    sin = 0
    for x in range(0, 32):
        sin += data_sin32[x]

    axeFreq = (t3 * fe) / N

    for y in data_sin32:
        Freq_amp.append(data_fft_abs[y])
        Freq_phase.append(data_fft_ang[y])
        Freq_Harm.append(axeFreq[y])

    Freq0 = axeFreq[data_sin32[0]]

    ReHarm = []
    ReDHarm = []
    MiHarm = []
    FaHarm = []
    SolHarm = []
    LadHarm = 1 * Freq_Harm





    for z in Freq_Harm:
        ReHarm.append(z * np.power(2.0, -8.0 / 12))
        ReDHarm.append(z * np.power(2.0, -7.0 / 12))
        MiHarm.append(z * np.power(2.0, -6.0 / 12))
        FaHarm.append(z * np.power(2.0, -5.0 / 12))
        SolHarm.append(z * np.power(2.0, -3.0 / 12))

    newSinRe = np.zeros(len(enveloppe))
    newSinReD = np.zeros(len(enveloppe))
    newSinMi = np.zeros(len(enveloppe))
    newSinFa = np.zeros(len(enveloppe))
    newSinLad = np.zeros(len(enveloppe))
    newSinSol = np.zeros(len(enveloppe))


    for w in range(0, 32):
        newSinRe += newNote(ReHarm[w], Freq_amp[w], fe, Freq_phase[w], enveloppe.size)
        newSinReD += newNote(ReDHarm[w], Freq_amp[w], fe, Freq_phase[w], enveloppe.size)
        newSinMi += newNote(MiHarm[w], Freq_amp[w], fe, Freq_phase[w], enveloppe.size)
        newSinFa += newNote(FaHarm[w], Freq_amp[w], fe, Freq_phase[w], enveloppe.size)
        newSinSol += newNote(SolHarm[w], Freq_amp[w], fe, Freq_phase[w], enveloppe.size)
        newSinLad += newNote(LadHarm[w], Freq_amp[w], fe, Freq_phase[w], enveloppe.size)

    Re = newSinRe * enveloppe
    ReD = newSinReD * enveloppe
    Mi = newSinMi * enveloppe
    Fa = newSinFa * enveloppe
    Sol = newSinSol * enveloppe
    LAd = newSinLad * enveloppe

    beginning = 8500
    tempo = 25000

    noteFreqs = {
        "C4": 261.60,
        "C#4": 277.20,
        "D4": Re[beginning:beginning+tempo],
        "D#4": ReD[beginning:beginning+tempo],
        "E4": Mi[beginning:beginning+tempo],
        "F4": Fa[beginning:beginning+tempo],
        "F#4": 370.00,
        "G4": Sol[beginning:beginning+tempo],
        "G#4": 415.30,
        "A4": 440.00,
        "A#4": 466.20,
        "B4": 493.90
    }

    noteBeats = {
        "whole": 2000,
        "half": 1000,
        "quarter": 500,
        "eigth": 250
    }

    # cinquiemeSymphonie = ["G4", "G4", "G4", "D#4", "D#4", "D#4", "F4", "F4", "F4", "D4", "D4", "D4"]
    cinquiemeSymphonie = ["G4", "G4", "G4", "D#4", "silence", "silence", "F4", "F4", "F4", "D4"]

    song = []
    # for k in range(25):
    #     for i in range(len(track_test)): # pas ici
    #         note = track_test[i]
    #         for j in range(len(noteFreqs[note])):
    #             song.append(noteFreqs[note][j])

    for i in range(len(cinquiemeSymphonie)):
        note = cinquiemeSymphonie[i]
        if note == "silence":
            for j in range(tempo):
                song.append(0)
        else:
            for j in range(len(noteFreqs[note])):
                song.append(noteFreqs[note][j])

    print(song)

    wave_write('song.wav', fe, song)

    # wave_write('LAd.wav', fe, LAd)
    # wave_write('Sol.wav', fe, Sol)
    # wave_write('Mi.wav', fe, Mi)
    # wave_write('Fa.wav', fe, Fa)
    # wave_write('Re.wav', fe, Re)

    plt.figure()
    # plt.plot(time[:480000], song)
    plt.title('La Diese')

    plt.figure()
    plt.plot(time, data)
    plt.ylabel('Amplitude')
    plt.xlabel('Temps (s)')
    plt.title('Spectre des amplitudes Fourier (LA#)')

    plt.figure()
    plt.plot(omega_b[80000:], FreqLog)
    plt.title('Sinusoidal principal')

    plt.figure()
    plt.plot(enveloppe)
    plt.title('Enveloppe filtré')

    plt.show()


if __name__ == "__main__":
    main()
