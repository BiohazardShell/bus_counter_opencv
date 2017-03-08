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

people_list = np.array( [  ] )
people_in_bus = 0
img_w = 1280
img_h = 720

cam = picamera.PiCamera()
cam.resolution = (img_w, img_h)
cam.hflip = False
RAWcapture = PiRGBArray( cam, size=( img_w, img_h ) )



# defining fonctions
def update_output( number ) :
	print(" people in the bus : %s", number )

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

def set_zone( people_list) :
	for i in range(0, len( people_list ) ) :
		if ( people_list[ i ]['zone'] != 'N' ) :
			if ( people_list[ i ]['zone'] == 'B' and people_list[ i ]['x'] > ( img_w / 2 ) ) :
				people_in_bus = people_in_bus + 1
				# suppr array case
				index = np.argwhere( people_list == i )
				people_list = np.delete( people_list, index )
			elif ( people_list[ i ]['zone'] == 'R' and people_list[ i ]['x'] < ( img_w / 2 ) ) :
				people_in_bus = people_in_bus - 1
				# suppr array case
				index = np.argwhere( people_list == i )
				people_list = np.delete( people_list, index )
			
		
	


while ( running ) :
	current_img = get_img()

	if (debugging) :
		cv2.rectangle( current_img, (0, 0), (img_w / 2, img_h), (255, 0, 0), 6 )
		cv2.rectangle( current_img, (img_w / 2, 0), (img_w, img_h), (0, 0, 255), 6 )
		debug_img_show( "raw rgb image", current_img )

	frontfaces_detected = detect_frontface( current_img )
	profilefaces_detected = detect_profileface( current_img )

	print( len( frontfaces_detected ) + len( profilefaces_detected ) )

	if (debugging) :
		if ( len( frontfaces_detected ) != 0 ) :
			for (x, y, w, h) in frontfaces_detected :
				print("x: %s   y: %s ", x, y)
				cv2.rectangle( current_img, (x, y), (x + w, y + h), (0, 255, 0), 2 )
	
		if ( len( profilefaces_detected ) != 0 )  :
			for (x, y, w, h) in profilefaces_detected :
				print("x: %s   y: %s ", x, y)
				cv2.rectangle( current_img, (x, y), (x + w, y + h), (0, 255, 0), 2 )
	
		debug_img_show( "rects for fullbody", current_img )



	people_count = 0
	if ( len( frontfaces_detected ) != 0 ) :
		for (x, y, w, h) in frontfaces_detected :
			people_list = np.append( people_list, { 'x':x, 'y':y, 'zone':'N' } )
			if (debugging) :
				print people_list
				cv2.waitKey(0)
			people_count = people_count + 1

	if ( len( profilefaces_detected ) != 0 ) :
		for (x, y, w, h) in profilefaces_detected :
			people_list = np.append(people_list, { 'x':x, 'y':y, 'zone':'N' } )
			if (debugging) :
				print people_list
				cv2.waitKey(0)
			people_count = people_count + 1

	set_zone( people_list )
	update_output( people_in_bus )
# redo
