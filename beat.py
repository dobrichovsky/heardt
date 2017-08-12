# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import strip
from neopixel import *
from scipy import signal

class Beat():
	
	s = strip.Strip()
	first = range(0, 600)
	second = range(700, 1050)
	third = range(600, 700)
	gFirst = signal.gaussian(len(first), std=40)	
	gSecond = signal.gaussian(len(second), std=40)
	gThird = signal.gaussian(len(third), std=40)
	frame = 0
	fps = 24
	maxBrightness = 128
	minBrightness = 0.05
	sector1 = [0.0, 0.0, 1.0, 0.66, 0.33, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	sector2 = [0.0, 0.0, 0.0, 0.0, 1.0, 0.66, 0.33, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	sector3 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	
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
		for i in self.third:
			self.s.strip.setPixelColor(i,Color(int(self.maxBrightness*self.sector3[self.frame]),0,0))
		self.s.strip.show()
		self.frame = self.frame + 1		
		if self.frame >= self.fps:
			self.frame = 0
	
# Main program logic follows:
if __name__ == '__main__':
	beat = Beat()
	print beat.gFirst
	start = time.clock()
	counter = 0	
	heartrate = 75	
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
