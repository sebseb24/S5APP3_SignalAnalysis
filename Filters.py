import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

import SoundGenerator as soundGenerator
import FileManager as fileManager


# Creation du signal sinusoidale avec les parametres de chaque harmonique
def newNote(freq, amp, rate, phase, tailles):
    taille = np.arange(tailles, dtype=float) / rate
    note = amp * np.sin(2 * np.pi * freq * taille + phase)
    return note

def fft(dataLa, NLa):
    han = np.hanning(NLa)
    fft = han*dataLa
    fft = np.fft.fft(fft, NLa)
    fft_abs = np.abs(fft)
    fft_ang = np.angle(fft)
    return fft_abs, fft_ang

def time(teLA, nLA):
    time = np.zeros(nLA)
    for k in range(nLA):
        time[k] = teLA*k
    return time

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


def extractionParametres(graphicsOn=False):
    # Extraction des parametres
    feLA, dataLA = fileManager.waveRead("note_guitare_LAd.wav")
    nLA = dataLA.size
    NLA = nLA
    t = 1.0 * nLA / feLA
    teFA = 1.0 / feLA
    t2_LA = np.arange(-nLA / 2, nLA / 2, 1)
    t3 = np.arange(0, nLA, 1, dtype=float)
    omega_b_LA = (t2_LA/NLA)*feLA

    Freq_amp = []
    Freq_phase = []
    Freq_Harm = []

    timeLA = time(teFA, nLA)

    LAfft_abs, LAfft_ang = fft(dataLA, NLA)

    # concaténation des donnees 0 à 80 k centré a 0
    FreqLog_LA = 20 * np.log10(LAfft_abs[:80000])

    # Algorithme pour choisir l'ordre N du filtre RIF passe-bas
    # filtre passe bas
    # ohm_bar = np.pi / 1000
    # for N1 in range(1, 885):
    #     n1 = np.arange(0, N1-1, 1)
    #     passeBas = np.abs((1/N1)*(np.exp(-1j*(n1*ohm_bar))))
    #     print(N1, passeBas)

    N1 = 884
    n1 = np.arange(0, N1 - 1, 1)
    ohm_bar = np.pi / 1000
    passeBas = np.abs((1 / N1) * (np.exp(-1j * (n1 * ohm_bar))))
    w, h = signal.freqz(passeBas)

    affichage("Reponse en frequence du filtre RIF passe-bas", "Frequence (rad/ech)", "Amplitude (dB)", w, 20 * np.log10(abs(h)))

    # Creation de l'enveloppe
    hk = []
    for temp in range(0, N1):
        hk.append(1 / N1)

    enveloppe = signal.fftconvolve(np.abs(dataLA), hk)

    # Isolation des 32 harmoniques principales du signal
    data_sin32_LA, _ = signal.find_peaks(FreqLog_LA, distance=1730, prominence=10)

    # Extraction des parametres de chaque harmonique
    axeFreq = (t3 * feLA) / NLA
    for y in data_sin32_LA:
        Freq_amp.append(LAfft_abs[y])
        Freq_phase.append(LAfft_ang[y])
        Freq_Harm.append(axeFreq[y])

    # Confirmation de la frequence fondamentale
    Freq0 = axeFreq[data_sin32_LA[0]]

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
        newSinRe += newNote(ReHarm[w], Freq_amp[w], feLA, Freq_phase[w], enveloppe.size)
        newSinReD += newNote(ReDHarm[w], Freq_amp[w], feLA, Freq_phase[w], enveloppe.size)
        newSinMi += newNote(MiHarm[w], Freq_amp[w], feLA, Freq_phase[w], enveloppe.size)
        newSinFa += newNote(FaHarm[w], Freq_amp[w], feLA, Freq_phase[w], enveloppe.size)
        newSinSol += newNote(SolHarm[w], Freq_amp[w], feLA, Freq_phase[w], enveloppe.size)
        newSinLad += newNote(LadHarm[w], Freq_amp[w], feLA, Freq_phase[w], enveloppe.size)

    Re = newSinRe * enveloppe
    ReD = newSinReD * enveloppe
    Mi = newSinMi * enveloppe
    Fa = newSinFa * enveloppe
    Sol = newSinSol * enveloppe
    LaD = newSinLad * enveloppe

    # Generation de la chanson a partir du signal synthetique et enregistrement dans un fichier wav, avec choix des
    # parametres
    notes = [Re, ReD, Mi, Fa, Sol, LaD]
    beginning = 8500  # Debut de la trame > 0 pour attenuer l'attaque
    tempo = 23000  # Nombre de trames qui constitues la longueur d'un temps

    soundGenerator.generateSong(notes, beginning, tempo, feLA, soundGenerator.getSongChoice("cinquiemeSymphonie"))

    # Fonction qui permet d'enregistrer les notes individuelles dans un fichier wav
    # soundGenerator.waveWriteIndividualsNotes(fe, Re, ReD, Mi, Fa, Sol, LaD)

    #Spectre LA# synthétisé
    feLA_Synt, dataLA_Synt = fileManager.waveRead('LAd.wav', "out")
    nLA_Synt = dataLA_Synt.size
    NLA_Synt = nLA_Synt
    t2_LA_Synt = np.arange(-nLA_Synt / 2, nLA_Synt / 2, 1)
    omega_b_LA_Synt = (t2_LA_Synt/NLA_Synt)*feLA_Synt
    LAfft_abs_Synt, LAfft_ang_Synt = fft(dataLA_Synt, NLA_Synt)

    FreqLog_LA_Synt = 20 * np.log10(LAfft_abs_Synt[:80442])

    # Affichage des graphiques
    if graphicsOn:
        affichage('Spectre des amplitudes Fourier (LA#)', 'Temps (s)', 'Amplitude', timeLA, dataLA)
        affichage('Peaks (sinus principal)', 'Fréquence (Hz)', 'Amplitude db', omega_b_LA[80000:], FreqLog_LA)
        affichage1('Enveloppe filtré', 'Nombre d''échantillon', 'Amplitude', enveloppe)
        affichage('Peaks (sinus principal) LA# synthétisé', 'Fréquence (Hz)', 'Amplitude (db)', omega_b_LA_Synt[80441:], FreqLog_LA_Synt)
        affichage("Reponse en frequence du filtre RIF passe-bas", "Frequence (rad/ech)", "Amplitude (dB)", w, 20 * np.log10(abs(h)))
    plt.show()
