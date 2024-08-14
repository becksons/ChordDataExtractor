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
 
# using harmonic-percussive source separation function,extract melody info,
     
harmonic, percussive = librosa.effects.hpss(y)
 
# Extract pitches and magnitudes 
pitches, magnitudes = librosa.core.piptrack(y=harmonic, sr=sr)
 

# Create MIDI file
midi = MIDIFile(1)  
 
midi.addTempo(0, 0, 120)   
 

# Add notes to MIDI based on extracted pitches
for t in range(pitches.shape[1]):
    for pitch in pitches[:, t]:
        if pitch > 0:  # Filter out non-pitched frames
            midi.addNote(0, 0, int(librosa.hz_to_midi(pitch)), t, 1, 100)
 
# Save the MIDI file
with open("output.mid", "wb") as output_file:
    midi.writeFile(output_file)
 

# Load the new MIDI file into music21
score = converter.parse('output.mid')

#Extract the key of mp3 file
print(score.analyze('key'))
score.show('text')