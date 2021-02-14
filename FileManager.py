import wave
import struct
import SoundGenerator as sg


def getGuitarSound():
    return wave.open('Sounds/note_guitare_LAd.wav')


def getBassonSound():
    return wave.open('Sounds/note_basson_plus_sinus_1000_Hz.wav')


# https://stackoverflow.com/questions/33879523/python-how-can-i-generate-a-wav-file-with-beeps
def writeWavFile(sig, filename):
    wav_file = wave.open(filename, 'w')
    nchannels = 1
    sampwidth = 2
    nframes = len(sig)
    comptype = "NONE"
    compname = "not compressed"
    sample_rate = sg.getSampleRate()

    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    for sample in sig:
        wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))

    wav_file.close()

    print("Writing in wav file : " + filename)

    return
