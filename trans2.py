#!/usr/bin/env python
from os import environ, path
import os
import shutil

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from moviepy.editor import *

from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

model_path = get_model_path()

config = {
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'dict': os.path.join(model_path, 'cmudict-en-us.dict')
}

#file = "trumpshort.wav"
file = "forward.wav"
file = "firework.wav"


ps = Pocketsphinx(**config)
ps.decode(
    audio_file=file,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
)

words = {}
minframe = 1e10

for seg in ps.segments(detailed=True):
  #print(seg.start_frame, seg.end_frame, seg.word)
  print(seg)

  word, acc, start, end = seg

  word = word.split('(')[0]

  minframe = min(minframe, start)

  if word.isalpha():
    if not word in words:
      words[word] = []
    words[word].append(seg)

clip = AudioFileClip(file)

import wave
origAudio = wave.open(file,'rb')
frameRate = origAudio.getframerate()
nChannels = origAudio.getnchannels()
sampWidth = origAudio.getsampwidth()

print(origAudio.getparams())

shutil.rmtree('words/', ignore_errors=True)

for word in words:
  for i in range(len(words[word])):
    seg = words[word][i]
    _, acc, start, end = seg

    os.makedirs('words/%s'%word,exist_ok=True)

    segname = "words/%s/%d.wav"%(word,i)

    origAudio.setpos((start - minframe) * 160)
    chunkData = origAudio.readframes((end - start) * 160)

    chunkAudio = wave.open(segname,'wb')
    chunkAudio.setnchannels(nChannels)
    chunkAudio.setsampwidth(sampWidth)
    chunkAudio.setframerate(frameRate)
    chunkAudio.writeframes(chunkData)
    chunkAudio.close()


# print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])