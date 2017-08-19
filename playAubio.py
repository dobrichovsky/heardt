"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys
import numpy as np

from aubio import source, onset

win_s = 2048                 # fft size
hop_s = win_s // 2          # hop size

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

#wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

data = np.zeros((2048),dtype="int16")

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

o = onset("kl", win_s, hop_s, RATE)
#o.set_delay(30000)
#print o.get_minioi()
#o.set_minioi(500000)
#print o.get_minioi()
count = 0
last = 10
while stream.is_active():
	readdata = np.fromstring(data,dtype=np.int16).astype(np.float32)
	#time.sleep(0.1)
	left = readdata[::2]
	right = readdata[1::2]
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

