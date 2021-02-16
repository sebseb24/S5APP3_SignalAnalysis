import FileManager as fileManager


# Vitesse d'echantillonnage, defaut = 44100.0
sample_rate = 44100.0

cinquiemeSymphonie = [("G4", "half"), ("G4", "half"), ("G4", "half"), ("D#4", "whole"),
                      ("silence", "half"), ("F4", "half"), ("F4", "half"), ("F4", "half"), ("D4", "whole")]

songChoices = {
    "cinquiemeSymphonie": cinquiemeSymphonie
}


def getSongChoice(songName):
    return songChoices[songName]


def getSampleRate():
    return sample_rate


# Genere la chanson choisie avec la liste de notes generees par les filtres
def generateSong(notes, beginning, tempo, fe, songChoice):
    noteFreqs = {
        "C4": 261.60,
        "C#4": 277.20,
        "D4": notes[0][beginning:],
        "D#4": notes[1][beginning:],
        "E4": notes[2][beginning:],
        "F4": notes[3][beginning:],
        "F#4": 370.00,
        "G4": notes[4][beginning:],
        "G#4": 415.30,
        "A4": 440.00,
        "A#4": 466.20,
        "B4": 493.90
    }

    # Le demi-temps correspond a la mesure de base
    noteBeats = {
        "whole": 2 * tempo,
        "half": tempo,
        "quarter": tempo / 2,
        "eigth": tempo / 4
    }

    song = []
    for i in range(len(songChoice)):
        note = songChoice[i]
        length = noteBeats[note[1]]

        if note[0] == "silence":
            for j in range(int(length)):
                song.append(0)
        else:
            for j in range(int(length)):
                song.append(noteFreqs[note[0]][j])

    # Creation du fichier wav
    fileManager.waveWrite('song.wav', fe, song)


# Permet d'enregistrer les notes individuelles dans un fichier wav
def waveWriteIndividualsNotes(fe, Re, Mi, Fa, Sol, LaD):
    fileManager.waveWrite('Re.wav', fe, Re)
    fileManager.waveWrite('Mi.wav', fe, Mi)
    fileManager.waveWrite('Fa.wav', fe, Fa)
    fileManager.waveWrite('Sol.wav', fe, Sol)
    fileManager.waveWrite('LAd.wav', fe, LaD)
