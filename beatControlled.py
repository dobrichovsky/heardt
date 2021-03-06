import time
import strip
from recorder import Recorder
from neopixel import *
from scipy import signal
import numpy as np

LOWTHRESHOLD = 64
THRESHOLTMULTIPLIER = 1.0 * LOWTHRESHOLD / (256 - LOWTHRESHOLD)

class Beat():
	
	s = strip.Strip()
	first = range(0, 150)
	second = range(150, 250)
	third = range(250, 300)
	gFirst = signal.gaussian(len(first), std=10)	
	gSecond = signal.gaussian(len(second), std=10)
	frame = 0
	frames = 6
	fps = 24
	maxBrightness = 255
	minBrightness = 0.004
	sector1 = [1.0, 0.66, 0.33, 0.0, 0.0, 0.0]
	sector2 = [0.0, 0.0, 1.0, 0.66, 0.33, 0.0]
	
	flowframe = 0

	maxBeat = 180 #max heartbeat frequency when excersizing
	minBeat = 50 #for now, minimum beat frequency
	
	beatInProgress = False

	# Define functions which animate LEDs in various ways.
	def colorWipe(self, color, wait_ms=50):
		"""Wipe color across display a pixel at a time."""
		for i in range(self.s.strip.numPixels()):
			self.s.strip.setPixelColor(i, color)
			self.s.strip.show()
			time.sleep(wait_ms/1000.0)

	def off(self):
		for i in range(self.s.strip.numPixels()):
			self.s.strip.setPixelColor(i,Color(0,0,0))
		self.s.strip.show()
		
	def flowAnim(self, value=64):
		for i in range(self.third[0]+self.flowframe,self.third[-1],6):
			beat.s.strip.setPixelColor(i,Color(min(255,int(value))/2,0,0))
		for i in range(self.third[0]+self.flowframe+1,self.third[-1],6):
			beat.s.strip.setPixelColor(i,Color(min(255,int(value)),0,0))
		for i in range(self.third[0]+self.flowframe+2,self.third[-1],6):
			beat.s.strip.setPixelColor(i,Color(0,0,0))
		for i in range(self.third[0]+self.flowframe+3,self.third[-1],6):
			beat.s.strip.setPixelColor(i,Color(0,0,0))
		for i in range(self.third[0]+self.flowframe+4,self.third[-1],6):
			beat.s.strip.setPixelColor(i,Color(0,0,0))
		for i in range(self.third[0]+self.flowframe+5,self.third[-1],6):
			beat.s.strip.setPixelColor(i,Color(0,0,0))
		
		self.flowframe = self.flowframe + 1
		if self.flowframe >= 6:
			self.flowframe = 0
		
	
	def beatAnim(self):
		#print self.frame
		for i in self.first:
			self.s.strip.setPixelColor(i,Color(int(self.maxBrightness * (self.gFirst[i-self.first[0]] * self.sector1[self.frame] + self.minBrightness * (1-self.sector1[self.frame]))),0,0))
			#self.s.strip.setPixelColor(i,Color(int(self.maxBrightness * (self.gFirst[i-self.first[0]] * 1.0)),0,0))
		for i in self.second:
			self.s.strip.setPixelColor(i,Color(int(self.maxBrightness * (self.gSecond[i-self.second[0]] * self.sector2[self.frame] + self.minBrightness * (1-self.sector2[self.frame]))),0,0))
			#self.s.strip.setPixelColor(i,Color(int(self.maxBrightness * (self.gSecond[i-self.second[0]] * 1.0)),0,0))
		
	def oneBeat(self):
		self.beatInProgress = True
		self.frame = 0
		self.beatAnim()
		self.frame = self.frame + 1	
		
	def checkBeat(self):
		if self.beatInProgress:
			self.beatAnim()
			self.frame = self.frame + 1
			if self.frame >= self.frames:
				self.beatInProgress = False
				
	def show(self):
		self.s.strip.show()		
		
			
def sound2LED(value):
	return min(LOWTHRESHOLD,max(0,(value / 128 - LOWTHRESHOLD) * THRESHOLTMULTIPLIER))
	
# Main program logic follows:
if __name__ == '__main__':
	beat = Beat()
	recorder = Recorder()
	recorder.start()
	
	start = time.clock()
	count = 0
	fps = 0
	last = 10

	BUFFERSIZE = 43
	BEATBUFFERSIZE = 1024
	BEATCUTOFF = 128

	FASTACTIONSIZE = 1
	circularbuffer = np.zeros((BUFFERSIZE),dtype="float32")
	maxbuffer = np.zeros((BUFFERSIZE),dtype="float32")
	bufferpos = 0
	beatbufferpos = 0
	longtermbuffer = np.zeros((BUFFERSIZE),dtype="float32")
	beatbuffer = np.zeros((BEATBUFFERSIZE),dtype="float32")
	
	beatsPerMin = 30
	BPMdivisor = 280
	beatSpace = 60.0 / beatsPerMin
	
	lastBeat = time.clock()
	lastSample = lastBeat
	
	while recorder.stream.is_active():
		
		last = max(1,last-5)
		if True: #recorder.newData == True:
			#recorder.newData = False
			readdata = np.fromstring(recorder.data,dtype=np.int16).astype(np.float32)
			#time.sleep(0.001)
			left = readdata[::2]
			right = readdata[1::2]
			circularbuffer[bufferpos] = np.mean(abs(left))
			
			maxbuffer[bufferpos] = np.max(abs(left))
			longtermbuffer[bufferpos] = np.mean(circularbuffer)

			if sound2LED(circularbuffer[bufferpos]) > last:
				last = sound2LED(circularbuffer[bufferpos])
			if 0.5 * sound2LED(np.mean(longtermbuffer)) > last:
				last = sound2LED(np.mean(longtermbuffer)) * 0.5
				#print "longtime" + str(last) + " " + str(time.clock())
			
			bufferpos = bufferpos + 1
			if bufferpos >= BUFFERSIZE:
				bufferpos = 0
			
			
			#print beatbufferpos
			if beatbufferpos - BEATCUTOFF < 0:
				value = min(np.mean(beatbuffer), \
					np.mean(np.concatenate([beatbuffer[:beatbufferpos], \
					beatbuffer[BEATBUFFERSIZE+beatbufferpos-BEATCUTOFF:]]) \
					))
				beatsPerMin = value / BPMdivisor + 30
				#print "end " + str(np.mean(beatbuffer)) + " " + str(np.mean(np.concatenate([beatbuffer[:beatbufferpos], \
				#	beatbuffer[BEATBUFFERSIZE+beatbufferpos-BEATCUTOFF:]]) \
				#	)) 
			else:
				value = min(np.mean(beatbuffer),np.mean(beatbuffer[beatbufferpos-BEATCUTOFF:beatbufferpos]))
				beatsPerMin = value / BPMdivisor + 30
				#print "middle " + str(np.mean(beatbuffer)) + " " + str(np.mean(beatbuffer[beatbufferpos-BEATCUTOFF:beatbufferpos]))
				#print beatbuffer[beatbufferpos-BEATCUTOFF:beatbufferpos]
			beatSpace = 60.0 / beatsPerMin
			#print np.mean(beatbuffer)
			
			if time.clock() - beatSpace > lastBeat:
				lastBeat = time.clock()
				#print "beat " + str(time.clock()) + " " + str(beatsPerMin)
				beat.oneBeat()
				
			beat.checkBeat()
			beat.flowAnim(last)
			beat.show()
			
			if time.clock() - 1.0 / 24 > lastSample:
				beatbuffer[beatbufferpos] = circularbuffer[bufferpos]
				lastSample = time.clock()
				beatbufferpos = beatbufferpos + 1

			if beatbufferpos >= BEATBUFFERSIZE:
				beatbufferpos = 0
			
			now = time.clock()
			fps = fps + 1
			if now-start >= 1.0:
				peaksPerSecond = count
				count = 0
				print beatsPerMin
				#print str(peaksPerSecond) + "/" + str(fps)
				fps = 0
				
#				print str(np.mean(circularbuffer)) + "/" + str(np.mean(maxbuffer))
			
				start = now
		#print last
		#for i in range(beat.s.strip.numPixels()):
		#	beat.s.strip.setPixelColor(i,Color(min(255,int(last)),0,0))
		#beat.s.strip.show()
