import math

sample_rate = 44100.0

noteFreqs = {
    "C4": 261.60,
    "C#4": 277.20,
    "D4": 293.70,
    "D#4": 311.10,
    "E4": 329.60,
    "F4": 349.23,
    "F#4": 370.00,
    "G4": 392.00,
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

cinquiemeSymphonie = [("G4", "eigth"), ("G4", "eigth"), ("G4", "eigth"), ("D#4", "half"), ("silence", "eigth"),
                      ("F4", "eigth"), ("F4", "eigth"), ("F4", "eigth"), ("D4", "whole")]


def playSong(sig):
    for i in range(len(cinquiemeSymphonie)):
        note = cinquiemeSymphonie[i]
        if note[0] == "silence":
            generate_silence(sig, noteBeats[note[1]])
        else:
            generate_sinewave(sig, noteFreqs[note[0]], noteBeats[note[1]])

    return sig


def generate_sinewave(sig, freq=440.0, duration_milliseconds=500, volume=1.0):
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        sig.append(volume * math.sin(2 * math.pi * freq * (x / sample_rate)))

    return sig


def generate_silence(sig, duration_milliseconds=500):
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        sig.append(0.0)

    return sig


def getSampleRate():
    return sample_rate
