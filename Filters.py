import sys
import math
from math import sin, pi
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wave
from scipy import signal

import SoundGenerator as soundGenerator
import FileManager as fileManager


# Creation du signal sinusoidale avec les parametres de chaque harmonique
def newNote(freq, amp, rate, phase, tailles):
    taille = np.arange(tailles, dtype=float) / rate
    note = amp * np.sin(2 * np.pi * freq * taille + phase)
    return note


def extractionParametres():
    # Initialisation des variables
    fe, data = fileManager.waveRead("note_guitare_LAd.wav")
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

    # Extraction des parametres du son
    data_fft = np.fft.fft(data, N)
    data_fft_abs = np.abs(data_fft)
    data_fft_ang = np.angle(data_fft)

    # concaténation des donnees 0 à 80 k centré a 0
    FreqLog = 20 * np.log10(data_fft_abs[:80000])

    ############### Est ce qu'on garde ca ? ###############################
    # filtre passe bas
    # ohm_bar = np.pi / 1000
    # for N1 in range(1, 885):
    #     n1 = np.arange(0, N1-1, 1)
    #     passeBas = np.abs((1/N1)*np.sum(np.exp(-1j*(n1*ohm_bar))))
    #     print(N1, passeBas)

    # Algorithme pour choisir l'ordre N du filtre RIF passe-bas
    N1 = 884  # trouver grace a la boucle for
    # n1 = np.arange(0, N1-1, 1)
    # passeBas = np.abs((1 / N1) * np.sum(np.exp(-1j * (n1 * ohm_bar))))

    # Creation de l'enveloppe
    hk = []
    for temp in range(0, N1):
        hk.append(1 / N1)

    enveloppe = signal.fftconvolve(np.abs(data), hk)

    # Isolation des 32 harmoniques principales du signal
    data_sin32, _ = signal.find_peaks(FreqLog, distance=1735, prominence=17)

    # sin = 0
    # for x in range(0, 32):
    #     sin += data_sin32[x]

    # Extraction des parametres de chaque harmonique
    axeFreq = (t3 * fe) / N
    for y in data_sin32:
        Freq_amp.append(data_fft_abs[y])
        Freq_phase.append(data_fft_ang[y])
        Freq_Harm.append(axeFreq[y])

    # Confirmation de la frequence fondamentale
    Freq0 = axeFreq[data_sin32[0]]

    # Construction synthetique des autres notes a partir du LA diese obtenu
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
    LaD = newSinLad * enveloppe

    # Generation de la chanson a partir du signal synthetique et enregistrement dans un fichier wav, avec choix des
    # parametres
    notes = [Re, ReD, Mi, Fa, Sol, LaD]
    beginning = 8500    # Debut de la trame > 0 pour attenuer l'attaque
    tempo = 23000   # Nombre de trames qui constitues la longueur d'un temps

    soundGenerator.generateSong(notes, beginning, tempo, fe, soundGenerator.getSongChoice("cinquiemeSymphonie"))

    # Fonction qui permet d'enregistrer les notes individuelles dans un fichier wav
    # soundGenerator.waveWriteIndividualsNotes(fe, Re, ReD, Mi, Fa, Sol, LaD)

    # Affichage des graphiques
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
