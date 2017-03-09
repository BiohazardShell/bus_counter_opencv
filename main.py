import cv2
import picamera
from picamera.array import PiRGBArray
import numpy as np
import os, sys
from PIL import Image


# define vars
debugging = False
running = True

people_list = np.array( [  ] )
people_in_bus = 0
img_w = 1280
img_h = 720

cam = picamera.PiCamera()
cam.resolution = (img_w, img_h)
cam.hflip = False

# calassifier
frontfaces = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
profilefaces = cv2.CascadeClassifier('haarcascade_profileface.xml')

# defining fonctions
def update_output( number ) :
	print(" people in the bus : %s", number )

def get_img( RAWcapture ) :
	cam.capture(RAWcapture, format="bgr")
	img = RAWcapture.array
	return img

def debug_img_show(msg, img) :
	cv2.imshow( msg, img )
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def load_detected( haar, img ) :
	detected = haar.detectMultiScale( img )
	return detected

def detect_frontface( img ) :
	return load_detected( frontfaces, img )

def detect_profileface( img ) :
	return load_detected( profilefaces, img )

def set_zone( people_list) :
	for i in range(0, len( people_list ) ) :
		if ( people_list[ i ]['zone'] != 'N' ) :
			if ( people_list[ i ]['zone'] == 'B' and people_list[ i ]['x'] > ( img_w / 2 ) ) :
				people_in_bus = people_in_bus + 1
				index = np.argwhere( people_list == i )
				people_list = np.delete( people_list, index )
			elif ( people_list[ i ]['zone'] == 'R' and people_list[ i ]['x'] < ( img_w / 2 ) ) :
				people_in_bus = people_in_bus - 1
				index = np.argwhere( people_list == i )
				people_list = np.delete( people_list, index )
		if ( people_list[ i ]['zone'] == 'N' ) :
			if ( people_list[ i ]['x'] > ( img_w /2 ) ) :
				people_list[ i ]['zone'] = 'R'
			elif ( people_list[ i ]['x'] < ( img_w / 2 ) ) :
				people_list[ i ]['zone'] = 'B'
		
	


while ( running ) :
	raw = PiRGBArray( cam, size=( img_w, img_h ) )
	tmp_img = get_img( raw )
	current_img = tmp_img
	del raw

	if (debugging) :
		cv2.rectangle( current_img, (0, 0), (img_w / 2, img_h), (255, 0, 0), 6 )
		cv2.rectangle( current_img, (img_w / 2, 0), (img_w, img_h), (0, 0, 255), 6 )
		debug_img_show( "raw rgb image", current_img )

	frontfaces_detected = detect_frontface( cv2.cvtColor( tmp_img,  cv2.COLOR_BGR2GRAY) )
	profilefaces_detected = detect_profileface( cv2.cvtColor( tmp_img, cv2.COLOR_BGR2GRAY ) )

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
	if (debugging) :
		print people_list
	update_output( people_in_bus )
# redo
