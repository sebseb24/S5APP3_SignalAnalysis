import numpy as np
import scipy.io.wavfile as wave


# def getGuitarSound():
#     # return wave.open('Sounds/note_guitare_LAd.wav')
#     fe, data = wave.read('Sounds/note_guitare_LAd.wav')
#     return fe, data


# def getBassonSound():
#     return wave.open('Sounds/note_basson_plus_sinus_1000_Hz.wav')
#

def waveRead(filename):
    return wave.read('SoundsIn/' + filename)


def waveWrite(filename, rate, note):
    scaled = np.int16(note / np.max(np.abs(note)) * 32767)
    wave.write('SoundsOut/' + filename, rate, scaled)


# https://stackoverflow.com/questions/33879523/python-how-can-i-generate-a-wav-file-with-beeps
# def writeWavFile(sig, filename):
#     wav_file = wave.open(filename, 'w')
#     nchannels = 1
#     sampwidth = 2
#     nframes = len(sig)
#     comptype = "NONE"
#     compname = "not compressed"
#     sample_rate = sg.getSampleRate()
#
#     wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))
#
#     for sample in sig:
#         wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))
#
#     wav_file.close()
#
#     print("Writing in wav file : " + filename)
#
#     return
