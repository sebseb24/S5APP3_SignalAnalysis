import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wave
from scipy import signal

def wave_reading():
    rate, data = wave.read('note_basson_plus_sinus_1000_Hz.wav')
    return rate, data

def wave_writing(rate, basson):
    wave.write('newBasson.wav', rate, basson.astype(np.int16))

def main():
    #lecture du fichier .wav d'origine
    rate, data = wave_reading()

    # initialisation des variable
    N = 6000
    fe = N
    w0 = 2*np.pi*960/6000
    w1 = 2*np.pi*1040/6000

    f = (w1/(2*np.pi))*fe
    K = (f/fe)*N*2+1

    n = np.arange((-N / 2)+1, (N / 2)+1, 1)

    #passe bas
    h_n = (1 / N) * (np.sin(np.pi * n * K / N) / (np.sin(np.pi * n / N)))
    h_n[int(N/2-1)] = K / N

    #coupe bande
    delta_n = np.zeros(N)
    delta_n[int(N/2)] = 1
    hbs = delta_n - (2 * h_n * np.cos(w0*n))

    #convolution entre data et le coupe bande
    basson = np.convolve(data, hbs)

    for x in range(0,1):
        basson = np.convolve(basson,hbs)

    # ecriture dans le fichier .wav
    wave_writing(rate, basson)

if __name__ == '__main__':
    main()