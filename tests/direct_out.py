#!/bin/python

import pyaudio
from pylibpd import *
import numpy
import argparse

parser = argparse.ArgumentParser(description="Serves a Pure Data patch over HTTP.")
parser.add_argument("folder", type=str, help="path to the project's main.pd")
args = parser.parse_args()

def pd_receive(*s):
  print('received:', s)

libpd_set_print_callback(pd_receive)

in_chan = 0
out_chan = 2
sample_rate = 48000
ticks = 1

buffer_size = 1024

pd = PdManager(in_chan, out_chan, sample_rate, ticks)

patch = libpd_open_patch('main.pd',"./" + args.folder)

audio = pyaudio.PyAudio()

stream = audio.open(format = pyaudio.paInt16,
                    channels = out_chan,
                    rate = sample_rate,
                    output = True,
                    frames_per_buffer = buffer_size)

try:
    while True:
        raw = pd.process(b'\x00')
        stream.write(bytes(raw))
except KeyboardInterrupt:
    stream.close()
    audio.terminate()


