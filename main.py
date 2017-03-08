import cv2
import picamera
from picamera.array import PiRGBArray
import imutils
import numpy as np
import os, sys
from PIL import Image


# define vars
debugging = True
running = True

bg_filter = cv2.createBackgroundSubtractorMOG2( detectShadows=True )

cam = picamera.PiCamera()
cam.resolution = (1280, 720)
RAWcapture = PiRGBArray( cam, size=( 1280, 720 ) )




def get_img() :
	cam.capture(RAWcapture, format="rgb")
	img = RAWcapture.array
	return img

def debug_img_show(msg, img) :
	cv2.imshow( msg, img )
	cv2.waitKey(0)

def load_detected( xml, img ) :
	haar = cv2.CascadeClassifier( xml )
	detected = haar.detectMultiScale( img )
	return detected

def detect_upperbody( img ) :
	return load_detected('haarcascade_upperbody.xml', img)

def detect_fullbody( img ) :
	return load_detected('haarcascade_fullbody.xml', img)

def detect_lowerbody( img ) :
	return load_detected('haarcascade_lowerbody.xml', img)

def detect_frontface( img ) :
	return load_detected('haarcascade_frontalface_alt2.xml', img)

def detect_profileface( img ) :
	return load_detected('haarcascade_profileface.xml', img)


#while ( running ) :
current_img = get_img()

if (debugging) :
	debug_img_show( "raw rgb image", current_img )

frontfaces_detected = detect_frontface( current_img )
profilefaces_detected = detect_profileface( current_img )

print( len( frontfaces_detected ) + len( profilefaces_detected ) )

if (debugging) :
	for (x, y, w, h) in frontfaces_detected :
		print("x: %s   y: %s ", x, y)
		cv2.rectangle( current_img, (x, y), (x + w, y + h), (0, 255, 0), 2 )
	
	for (x, y, w, h) in profilefaces_detected :
		print("x: %s   y: %s ", x, y)
		cv2.rectangle( current_img, (x, y), (x + w, y + h), (0, 255, 0), 2 )
	
	debug_img_show( "rects for fullbody", current_img )


