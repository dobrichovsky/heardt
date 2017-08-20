import pyaudio
import time
import sys
import numpy as np

from aubio import onset

class Recorder():
	p = pyaudio.PyAudio()
	data = np.zeros((2048),dtype="int16")
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	CHUNK = 1024

	win_s = 2048                 # fft size
	hop_s = win_s // 2          # hop size

	def callback(self, in_data, frame_count, time_info, status):
	    self.data = in_data
	    return (self.data, pyaudio.paContinue)



	def start(self):
		self.stream = self.p.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
				stream_callback=self.callback)
		self.stream.start_stream()
		self.o = onset("kl", self.win_s, self.hop_s, self.RATE)

