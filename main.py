#!/bin/python

from flask import Flask, render_template, Response
from pylibpd import *
import numpy
import argparse
import sys 

parser = argparse.ArgumentParser(description="Serves a Pure Data patch over HTTP.")
parser.add_argument("folder", type=str, help="path to the project's main.pd")
args = parser.parse_args()

in_chan = 1
out_chan = 2
sample_rate = 44100
ticks = 1

buffer_size = 2048
out_buffer = numpy.zeros(buffer_size, numpy.int16)

def pd_receive(*s):
  print('received:', s)

libpd_set_print_callback(pd_receive)

pd = PdManager(in_chan, out_chan, sample_rate, ticks)

libpd_open_patch('main.pd', "./"+args.folder)

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', p_name=args.folder)

@app.route('/puredata')
def puredata():
    def compute():
        bitsPerSample = 16
        wav_header = genHeader(sample_rate, bitsPerSample, out_chan)
        first_run = True
        while True:
            #process pure data output;
            for i in range(buffer_size):
                pd_frame = i % (out_chan*ticks*64)
                if pd_frame == 0:
                    raw = pd.process(b'\x00')
                out_buffer[i] = raw[pd_frame]
            if first_run:
                data = wav_header + bytes(out_buffer)
                first_run = False
            else:
                data = bytes(out_buffer)
            yield(data)
    return Response(compute())

if __name__ == '__main__':
    app.run(host='192.168.15.94')
