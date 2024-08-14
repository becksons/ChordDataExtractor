import librosa
import numpy as np

from midiutil import MIDIFile
from music21 import converter
"""
    Convert MP3 to MIDI 
    *A script to extract chord information from mp3 files*
    
    Sources:
    https://librosa.org/doc/0.10.1/tutorial.html
    https://librosa.org/doc/0.10.1/generated/librosa.effects.hpss.html

"""

# Load the MP3 file using librosa
y, sr = librosa.load('/Users/becksonstein/Documents/BU/MIR/TestSong.mp3')
print("Checkpnt 1")
# using harmonic-percussive source separation function,extract melody info,
     
harmonic, percussive = librosa.effects.hpss(y)
print("Checkpnt 2")
# Extract pitches and magnitudes 
pitches, magnitudes = librosa.core.piptrack(y=harmonic, sr=sr)
print("Checkpnt 3")

# Create MIDI file
midi = MIDIFile(1)  
print("Checkpnt 4")
midi.addTempo(0, 0, 120)   
print("Checkpnt 5")

# Add notes to MIDI based on extracted pitches
for t in range(pitches.shape[1]):
    for pitch in pitches[:, t]:
        if pitch > 0:  # Filter out non-pitched frames
            midi.addNote(0, 0, int(librosa.hz_to_midi(pitch)), t, 1, 100)
print("Checkpnt 6")
# Save the MIDI file
with open("output.mid", "wb") as output_file:
    midi.writeFile(output_file)
print("Checkpnt 7")

# Load the MIDI file into music21
score = converter.parse('output.mid')
print("Checkpnt 8")
# Now you can analyze the score, extract key signatures, chords, etc.
print(score.analyze('key'))
score.show('text')