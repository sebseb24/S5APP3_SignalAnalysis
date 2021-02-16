import numpy as np
import scipy.io.wavfile as wave


# Lecture des fichiers wav entrants
def waveRead(filename, folder="in"):
    if folder == "out":
        return wave.read('SoundsOut/' + filename)
    else:
        return wave.read('SoundsIn/' + filename)


# Creation et ecriture dans un fichier wav
def waveWrite(filename, rate, note):
    scaled = np.int16(note / np.max(np.abs(note)) * 32767)
    wave.write('SoundsOut/' + filename, rate, scaled)
    print("Created wav file : " + filename)

