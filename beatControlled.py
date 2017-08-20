import time
import strip
from recorder import Recorder
from neopixel import *
from scipy import signal

class Beat():
	
	s = strip.Strip()
	first = range(0, 200)
	second = range(200, 350)
	gFirst = signal.gaussian(len(first), std=10)	
	gSecond = signal.gaussian(len(second), std=10)
	frame = 0
	fps = 24
	maxBrightness = 255
	minBrightness = 0.02
	sector1 = [1.0, 0.66, 0.33, 0.0, 0.0]
	sector2 = [0.0, 0.0, 1.0, 0.66, 0.33]

	maxBeat = 180 #max heartbeat frequency when excersizing
	minBeat = 50 #for now, minimum beat frequency

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
	
	def beatAnim(self):
		#print self.frame
		for i in self.first:
			self.s.strip.setPixelColor(i,Color(int(self.maxBrightness * (self.gFirst[i-self.first[0]] * self.sector1[self.frame] + self.minBrightness * (1-self.sector1[self.frame]))),0,0))
			#self.s.strip.setPixelColor(i,Color(int(self.maxBrightness * (self.gFirst[i-self.first[0]] * 1.0)),0,0))
		for i in self.second:
			self.s.strip.setPixelColor(i,Color(int(self.maxBrightness * (self.gSecond[i-self.second[0]] * self.sector2[self.frame] + self.minBrightness * (1-self.sector2[self.frame]))),0,0))
			#self.s.strip.setPixelColor(i,Color(int(self.maxBrightness * (self.gSecond[i-self.second[0]] * 1.0)),0,0))
		self.s.strip.show()
		self.frame = self.frame + 1		
		if self.frame >= self.fps:
			self.frame = 0
	
# Main program logic follows:
if __name__ == '__main__':
	beat = Beat()
	recorder = Recorder()
	
	start = time.clock()
	counter = 0

	while recorder.stream.is_active():
		readdata = np.fromstring(recorder.data,dtype=np.int16).astype(np.float32)
		#time.sleep(0.1)
		left = readdata[::2]
		right = readdata[1::2]
		avgdata = np.mean(left,right)
		#print len(left)
		#print len(right)
		#print len(readdata)
		last = max(10,last-10)
		#if np.mean(abs(readdata)) > 300:
		if o(left):
			print o.get_last_s()
			print str(count) + " " + str(o.get_last())
			#count = count + 1
			last = 128
		for i in range(strip.numPixels()):
			strip.setPixelColor(i,Color(last,0,0))
		strip.show()



	print ('Press Ctrl-C to quit.')
	while True:
		counter = counter + 1
		if time.clock() - start >= 10:
			#beat.fps = counter/10
			print beat.fps
			cycles = counter/10
			counter = 0
			start = time.clock()
#		beat.off()
		beat.beatAnim()
		#beat.colorWipe(Color(128,0,0))
