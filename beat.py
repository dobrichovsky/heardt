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
	first = range(0, 800)
	second = range(800, 1200)
	third = range(350, 350)
	gFirst = signal.gaussian(len(first), std=10)	
	gSecond = signal.gaussian(len(second), std=10)
	gThird = signal.gaussian(len(third), std=10)
	frame = 0
	fps = 24
	maxBrightness = 255
	minBrightness = 0.07
	sector1 = [0.0, 0.0, 1.0, 0.66, 0.33, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	sector2 = [0.0, 0.0, 0.0, 0.0, 1.0, 0.66, 0.33, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	sector3 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	
	allBeatAnimSeq = [0.05, 0.5, 1.0, 0.8, 0.6, 0.4, 0.2, 0.05]
	currentSegment = 0
	
	segments = [[0,9],[9,27],[27,46],[46,54],[54,58],[58,65],[65,82],[82,97],[97,108],[108,119],
		[119,135],[135,141],[141,153],[153,169],[169,178],[178,180],[180,189],[189,197],[197,211],
		[211,225],[225,239],[239,243],[243,256],[256,259],[259,265],[265,268],[268,275],[275,290],
		[290,300],[300,344],[344,344],[344,344],[344,344],[344,344],[344,353],[353,363],[363,378],[378,394],[394,394],
		[394,404],[404,417],[417,428],[428,442],[442,451],[451,469],[469,492],[492,505],[505,514],
		[514,532],[532,542],[542,568],[568,573],[573,584],[584,600],[600,613],[613,616],[616,620]
		]
	
	coords = [[0.4,0],[0.48,0.22],[0.52,0.66],[0.5,0.9],[0.28,0.96],[0.28,0.9],[0.48,0.84],[0.52,0.66],
		[0.72,0.4],[0.48,0.22],[0.66,0],[0.72,0.4],[0.8,0.5],[0.52,0.66],[0.8,0.88],[0.56,0.98],[0.55,0.99],
		[0.8,0.88],[0.82,0.72],[0.8,0.5],[0.96,0.3],[1.0,0.56],[1.0,0.63],[0.94,0.4],[0.95,0.36],[0.96,0.26],
		[0.95,0.3],[0.95,0.36],[0.76,0],[0.96,0.26],[0.72,0.4],[0.72,0.4],[0.72,0.4],[0.72,0.4],[0.72,0.4],[0.8,0.5],
		[0.8,0.72],[0.52,0.66],[0.02,0.54],[0.48,0.22],[0.36,0.34],[0.36,0],[0.06,0.25],[0.02,0.54],[0.16,0.34],
		[0.52,0.66],[0.04,0.66],[0.02,0.54],[0,0.59],[0.06,0.25],[0.1,0],[0,0.59],[0.03,0.66],[0.2,0.8],[0.52,0.66],
		[0.36,0.82],[0.28,0.81],[0.36,0.78]
		]
	lightup = None
	
	def getPixel(self,num):
		seg = None
		segnum = 0
		for i in self.segments:			
			#print i
			#print i[0]
			if i[0] >= num:
				seg = i				
				break
			segnum = segnum + 1
		#print seg[1]
		if seg == None:
			return [0,0]
		#print seg
		if seg[1]==seg[0]:
			return [0,0]
		#######
		# there may be a mistake somewhere here #
		length = seg[1]-seg[0]
		#print length
		grad = 1.0 * (num - seg[0]) / length
		
		#print seg[1]
		#print self.coords[seg[1]][0]
		dx = self.coords[segnum+1][0] - self.coords[segnum][0]
		dy = self.coords[segnum+1][1] - self.coords[segnum][1]
		#print dx
		#print dy
		#print grad
		#print self.coords[segnum][0] + grad*dx
		return [self.coords[segnum][0] + grad*dx, self.coords[segnum][1] + grad*dy]
		#return [0,0]
	
	def __init__(self):
		#self.lightup = self.getLastRange()
		self.lightup = []
	
	def getLastRange(self):
		#return range(self.segments[-1][0],self.segments[-1][1])
		return range(self.segments[len(self.coords)-1][0],self.segments[len(self.coords)-1][1])
	
	def getRange(self, segment):
		return range(self.segments[segment][0],self.segments[segment][1])
	
	
	
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
		
	def lowRed(self):
		for i in range(self.s.strip.numPixels()):
			self.s.strip.setPixelColor(i,Color(64,0,0))
		self.s.strip.show()
		
	def white(self):
		for i in range(self.s.strip.numPixels()):
			self.s.strip.setPixelColor(i,Color(255,255,255))
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
			
	def allBeatAnim(self):
		for i in range(self.s.strip.numPixels()):
			self.s.strip.setPixelColor(i,Color(int(255*self.allBeatAnimSeq[min(self.frame,7)]),0,0))
		self.s.strip.show()
		
		self.frame = self.frame + 1		
		if self.frame >= self.fps:
			self.frame = 0
			
	def lightSegment(self):
		for i in range(self.s.strip.numPixels()):
			self.s.strip.setPixelColor(i,Color(0,0,0))
		for i in self.lightup:
			self.s.strip.setPixelColor(i,Color(128,0,0))
		self.s.strip.show()
		
		
	def cycleSegments(self):		
		for i in range(self.s.strip.numPixels()):
			self.s.strip.setPixelColor(i,Color(0,0,0))
		for i in self.getRange(self.currentSegment):
			self.s.strip.setPixelColor(i,Color(128,0,0))
		self.s.strip.show()
		self.currentSegment = self.currentSegment + 1
		if self.currentSegment >= len(self.segments):
			self.currentSegment = 0
			
	def triColor(self):
		for i in range(self.s.strip.numPixels()):
			self.s.strip.setPixelColor(i,Color(0,0,0))
		for i in range(620):
			pixel = self.getPixel(i)
			self.s.strip.setPixelColor(i,Color(max(min(255,int(pixel[1]*32)),0),0,0))
			#if pixel[1] < 0.33:
			#	self.s.strip.setPixelColor(i,Color(255,0,0))
			#elif pixel[1] < 0.66:
			#	self.s.strip.setPixelColor(i,Color(255,255,255))
			#else:
			#	self.s.strip.setPixelColor(i,Color(0,0,255))
		self.s.strip.show()
			
# Main program logic follows:
if __name__ == '__main__':
	beat = Beat()
	#print beat.gFirst
	start = time.clock()
	counter = 0	
	heartrate = 75	
	#print ('Press Ctrl-C to quit.')
	if len(beat.lightup) > 0:
		print beat.lightup[0]
	while True:
		counter = counter + 1
		if time.clock() - start >= 1:
			#beat.fps = counter/10
			#print beat.fps
			cycles = counter
			counter = 0
			start = time.clock()
			break
		
		#beat.cycleSegments()
		#beat.lightSegment()
		beat.triColor()
		#beat.allBeatAnim()
		#beat.off()
		#beat.beatAnim()
		#beat.lowRed()
#		beat.white()
		#beat.colorWipe(Color(128,0,0))
		
	
