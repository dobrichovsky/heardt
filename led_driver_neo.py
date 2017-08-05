# Will Yager
# This Python script sends color/brightness data based on
# ambient sound frequencies to the LEDs.

import pyaudio as pa
import numpy as np
import sys
# Output values max at 1.0
import notes_scaled_nosaturation
import lavalamp_colors
import math

import time

from neopixel import *

# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
#LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN        = 21    # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000 # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 6       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RBG   # Strip type and colour ordering

# define callback (2)
def callback(in_data,frame_count, time_info, status):
    global recorded
    recorded = np.fromstring(in_data,dtype=np.int16).astype(np.float)
    return (recorded, pa.paContinue)

audio_stream = pa.PyAudio().open(format=pa.paInt16, \
								channels=2, \
								rate=44100, \
								input=True, \
								# Uncomment and set this using find_input_devices.py
								# if default input device is not correct
								#input_device_index=2, \
								frames_per_buffer=8192,
								stream_callback=callback)

recorded = np.empty((8192),dtype="int16")
audio_stream.start_stream()


# Convert the audio data to numbers, num_samples at a time.
def read_audio(audio_stream, num_samples):
	global recorded
	while True:
		# Read all the input data. 
		#samples = audio_stream.read(num_samples,exception_on_overflow=False) 
		samples = recorded
		# Convert input data to numbers
		#samples = np.fromstring(samples, dtype=np.int16).astype(np.float)
		samples_l = samples[::2]  
		samples_r = samples[1::2]
		yield (samples_l, samples_r)

if __name__ == '__main__':
	
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	
	audio = read_audio(audio_stream, num_samples=512)
	#leds = notes_scaled_nosaturation.process(audio, num_leds=32, num_samples=512, sample_rate=44100)
	#colors = lavalamp_colors.colorize(leds, num_leds=32)
	
	#maxintensity = max(leds)
	
	start = time.clock()
	counter = 0
	
	timeout = 1.0
	cycles = 40
	fq = 0
	lastval = 0
	lastvalm = 0
	minimum = 2
	step = 0.1
	
	for l,r in audio:
		counter = counter + 1
		if time.clock() - start >= 10:
			print counter/10
			cycles = counter/10
			counter = 0
			start = time.clock()
		
		#lmax = max(l)*255.0
		amplitude = max(abs(l))/128.0
		#dB = 20 * math.log10(amplitude)
		#lmax = dB
		lmax = amplitude
		#print lmax
		#print str(lmax)+","+str(lastvalm)
		if lastval - step > minimum:
			lastval = lastval - step
		if lastvalm > 10:
			lastvalm = lastvalm - step
			#lastvalm = lastvalm - 0.5	
		if lmax > lastvalm:
			#print lmax
			lastval = lmax
			lastvalm = lmax
			step =  max(minimum,lastval - minimum) / (1.0 * cycles * timeout)
			#print step
		#print lastval
		for i in range(strip.numPixels()):
			strip.setPixelColor(i,Color(int(lastval),0,0))
		#print lastval
		strip.show()
			
		#time.sleep(20/1000.0)
