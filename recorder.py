import pyaudio
import time
import sys
import numpy as np

from aubio import onset

class Recorder():
	def __init__(self):
		self.p = pyaudio.PyAudio()
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 2
		self.RATE = 44100
		self.CHUNK = 4096
		self.data = np.zeros((2*self.CHUNK),dtype="int16")

		self.win_s = 2048                 # fft size
		self.hop_s = self.win_s // 2          # hop size
		self.stream = None
		self.o = None
		self.newData = False
	
	def get_callback(self):
		def callback(in_data, frame_count, time_info, status):
			self.data = in_data
			#self.newData = True
			return (self.data, pyaudio.paContinue)
		return callback
	
	def start(self):
		self.stream = self.p.open(format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
				stream_callback=self.get_callback())
		self.stream.start_stream()
		self.o = onset("default", self.win_s, self.hop_s, self.RATE)

