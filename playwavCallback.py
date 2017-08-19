"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys
import numpy as np

from neopixel import *

# LED strip configuration:
LED_COUNT      = 350      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 21    # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000 # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 6       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RBG   # Strip type and colour ordering

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

data = np.zeros((4096),dtype="int16")

#data = ""

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    global data
    #data = wf.readframes(frame_count)
    data = in_data
    return (data, pyaudio.paContinue)

# open stream using callback (3)
#stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                channels=wf.getnchannels(),
#                rate=wf.getframerate(),
#                output=True,
#                stream_callback=callback)
              
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
				stream_callback=callback)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
strip.begin()

# start the stream (4)
stream.start_stream()

timeout = 1.0
cycles = 24
fq = 0
lastval = 0
lastvalm = 0
minimum = 1
step = 0.1
lmax = 0
iteration = 0
counter = 0
start = time.clock()

CBUFFERSIZE = 43
C_MULTIPLIER = -0.0000015
C_ADDER = 1.5142857
  
circularbuffer = np.empty((CBUFFERSIZE),dtype="float32")
bufferpos = 0

# wait for stream to finish (5)
while stream.is_active():
	counter = counter + 1
	if time.clock() - start >= 10:
		#print counter/10
		cycles = counter/10
		counter = 0
		start = time.clock()
	lmax = np.mean(abs(np.fromstring(data,dtype=np.int16).astype(np.float)))/128.0
	readdata = np.fromstring(data,dtype=np.int16).astype(np.float)
	Ej = sum(readdata*readdata)
	#print Ej
	circularbuffer[bufferpos] = Ej
	avgE = 1.0/CBUFFERSIZE*sum(circularbuffer)
	#varE = 1.0/CBUFFERSIZE*sum((avgE-circularbuffer)*(avgE-circularbuffer))
	#C = C_MULTIPLIER * varE + C_ADDER
	C = 5.0
#	print avgE-circularbuffer
#	print circularbuffer
#	print str(Ej) + ", " + str(avgE) + ", " + str(varE)
	if Ej > C*avgE:
		print "beat " + str(Ej) + ">" + str(C*avgE)
		lmax = 255
	bufferpos = bufferpos + 1
	if bufferpos >= CBUFFERSIZE:
		bufferpos = 0
	if lastval - step > minimum:
		lastval = lastval - step
	if lastvalm > 10:
		lastvalm = lastvalm - step
		lastvalm = lastvalm - 0.5	
	if lmax > lastvalm:
		#print str(lmax)
		lastval = lmax
		lastvalm = lmax
		step =  max(minimum,lastval - minimum) / (0.02 * cycles * timeout)
	for i in range(strip.numPixels()):
		strip.setPixelColor(i,Color(max(min(int(lastval),255),5),0,0))
	strip.show()

# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()
