import cv2
import picamera
from picamera.array import PiRGBArray
import os, sys
import dlib
from PIL import Image

debugging = True
running = True

tracker = dlib.correlation_tracker()
people_tracked = 0

img_w = 1280
img_h = 720

cam = picamera.PiCamera()
cam.resolution = ( img_w, img_h )
cam.hflip = True
cam.vflip = True

def get_img( RAWCapture ) :
	cam.capture( RAWCapture, format="bgr" )
	img = RAWCapture.array
	return img

def update_output( number ):
	print( " People in the bus : %s ", number )

