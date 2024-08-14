from chord_extractor.extractors import Chordino
import matplotlib.pyplot as plt
from music21 import *
import librosa
import librosa.display
import pandas as pd
import numpy as np
from itertools import cycle
import seaborn as sns
from glob import glob

"""
    Chord Information Extractor
    *A script to extract chord information from mp3 files*
     Sources:
        
        https://stackoverflow.com/
        https://www.kaggle.com/code/robikscube/working-with-audio-in-python
    

"""

sns.set_theme(style="white", palette=None)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])

#load mp3 file
song = '/Users/becksonstein/Documents/BU/MIR/TestSong.mp3'
audio_files = glob(song)
chordino = Chordino(roll_on=1)

chords = chordino.extract(song)

y, sr = librosa.load(audio_files[0])
y_trimmed, _ = librosa.effects.trim(y, top_db=20)

 
pd.Series(y_trimmed).plot(figsize=(10, 5), lw=1, title='Trimmed Audio File', color=color_pal[1])

#Mel spectrogram
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128 * 2)
S_db_mel = librosa.amplitude_to_db(S, ref=np.max)
fig, ax = plt.subplots(figsize=(10, 5))
img = librosa.display.specshow(S_db_mel, x_axis='time', y_axis='log', ax=ax)
ax.set_title('Spectrogram of ' + 'TestSong', fontsize=20)
fig.colorbar(img, ax=ax, format=f'%0.2f')
# plt.show()

# Preprocess and clean chords
def preprocess_chord(ch):
    ch = ch.strip().capitalize()
   
    if "bm" in ch.lower():
        ch = ch.replace("bm", "Bbm")
    if "bb" in ch.lower():
        ch = ch.replace("bb", "Bb")
     
    if "m" in ch and ch[0].upper() in "ABCDEFG":
        if ch[1] == "b" or ch[1] == "#":
            return ch[0].upper() + ch[1] + ch[2:]
        else:
            return ch[0].upper() + "m"
    return ch

def clean_chords(chords):
    res = []
    for c in chords:
        if "/" in c:
            n1, _ = c.split("/")
            res.append(n1)
        elif c == "Bbm7":
            res.append(c[:-1])   
        else:
            res.append(c)
    return res
 
def identify_key(chords):
    chord_objects = []
    for ch in chords:
        try:
            preprocessed_chord = preprocess_chord(ch)
            chord_objects.append(chord.Chord(preprocessed_chord))
        except Exception as e:
            print(f"Error processing chord '{ch}': {e}")
            return None
    
    
    key_candidates = []
    for k in key.Key.allKeys():
        score = 0
        for c in chord_objects:
            if c.root().name in k.getScale().pitches:
                score += 1
        key_candidates.append((k, score))
     
  
    key_candidates.sort(key=lambda x: x[1], reverse=True)
    return key_candidates[0][0]
def count_chord(n, clist):
    count = 0
    for i in range(len(clist)):
        if n in clist[i][0]:
            count= count + 1
    return count

def get_chords(clist):
    chords = []
    for i in range(len(clist)):
        if clist[i][0] not in chords and clist[i][0] != 'N':
            chords.append(clist[i][0])
        else:
            continue
    return chords
def chord_freq(clist):
    c_freq = {}
    for i in range(len(clist)):
        c_freq.update({clist[i]: count_chord(clist[i],chords)})
    return c_freq
def suggest_scales(chords):
    key = identify_key(chords)
    if key:
        print(f"The key of the song is likely: {key.name}")
        scales = key.getScale()
        print(f"Suggested scales to play over the chords: {scales}")
 
chord_list = clean_chords(get_chords(chords))
print(chord_list)
print(identify_key(chord_list))
suggest_scales(chord_list)
 
chord_freq_dic = chord_freq(chord_list)
x = list(chord_freq_dic.keys())
y = list(chord_freq_dic.values())

plt.bar(x, y)
plt.xlabel('Chord')
plt.ylabel('Occurrences')
plt.show()
