# Simple code to open an image and provide a simple GUI to calibrate the color range for color detection
# This code uses OpenCV to create a simple GUI with trackbars to adjust the HSV color range
# Imports
import cv2  
import numpy as np

# Path to the image file
# You can change this path to any image you want to test
# path = "TestingImages\\2023-Cone\\frame0.jpg"
path = "TestingImages\\2024-Ring\\frame0.png"

#trackbar callback fucntion to update HSV value
def callback(x):
	global H_low, H_high, S_low, S_high, V_low, V_high
	
	#assign trackbar position value to H,S,V High and low variable
	H_low = cv2.getTrackbarPos('low H', 'controls')
	H_high = cv2.getTrackbarPos('high H', 'controls')
	S_low = cv2.getTrackbarPos('low S', 'controls')
	S_high = cv2.getTrackbarPos('high S', 'controls')
	V_low = cv2.getTrackbarPos('low V', 'controls')
	V_high = cv2.getTrackbarPos('high V', 'controls')


#create a seperate window named 'controls' for trackbar
cv2.namedWindow('controls', 2)
# cv2.resizeWindow("controls", 550, 50)

#global variable
H_low = 0
H_high = 179
S_low = 0
S_high = 255
V_low = 0
V_high = 255

#create trackbars for high,low H,S,V 
cv2.createTrackbar('low H', 'controls', 0, 179, callback)
cv2.createTrackbar('high H', 'controls', 179, 179, callback)

cv2.createTrackbar('low S', 'controls', 0, 255, callback)
cv2.createTrackbar('high S', 'controls', 255, 255, callback)

cv2.createTrackbar('low V', 'controls', 0, 255, callback)
cv2.createTrackbar('high V', 'controls', 255, 255, callback)

# Initialize the trackbars
while(1):
	#read source image
	img=cv2.imread(path)
	#convert sourece image to HSC color mode
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	#
	hsv_low = np.array([H_low, S_low, V_low], np.uint8)
	hsv_high = np.array([H_high, S_high, V_high], np.uint8)

	#making mask for hsv range
	mask = cv2.inRange(hsv, hsv_low, hsv_high)
	
	#print (mask)
	#masking HSV value selected color becomes black

	
	# Threshold the mask to create a binary image
	_, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # Define the kernel for the morphological operation
	kernel = np.ones((5, 5), np.uint8)

    # Perform morphological opening to remove noise
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Perform morphological closing to close small holes
    # This really helps to cleanup the mask
	processed_img = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

	res = cv2.bitwise_and(img, img, mask=processed_img)
	#show image
	cv2.imshow('mask',processed_img)
	cv2.imshow('res',res)
	
	#waitfor the user to press escape and break the while loop 
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break
		
#destroys all window
cv2.destroyAllWindows()