import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import wave

import FileManager as fileManager
import SoundGenerator as soundGenerator


if __name__ == '__main__':
    # guitarNote = fileManager.getGuitarSound()
    # bassonNote = fileManager.getBassonSound()
    #
    # raw = guitarNote.readframes(-1)
    # raw = np.frombuffer(raw, "int16")
    #
    # N = 160000
    #
    # plt.figure()
    # plt.plot(raw, color="blue")
    # plt.title("Raw signal")
    #
    # # h_n = np.hanning(N)
    # # raw_hn = raw*h_n
    # raw_fft = np.fft.fft(raw)
    # sig = np.abs(raw_fft)
    # sig_angle = np.angle(raw_fft)
    # sig_rad = np.radians(sig_angle)
    #
    # plt.figure()
    # plt.stem(sig)
    # plt.title("Amplitude after fft")
    #
    # plt.figure()
    # plt.stem(sig_rad)
    # plt.title("Angle after fft")

    sig = []

    # soundGenerator.generate_sinewave(sig)
    # soundGenerator.generate_silence(sig)
    # soundGenerator.generate_sinewave(sig)
    # soundGenerator.generate_silence(sig)
    # soundGenerator.generate_sinewave(sig)
    soundGenerator.playSong(sig)
    fileManager.writeWavFile(sig, "wavOut.wav")

    plt.show()

    exit(1)
