from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2
import math
#approx human height in cm.
H = 168
FAR = 140
def caldist(rect1,rect2):
	
	rat1 = (H / (rect1[1]+rect1[3]))
	rat2 = (H / (rect2[1]+rect2[3]))
	ratAvg = (rat1 + rat2)/2
	a = rat1*(rect1[3] - rect2[3])
	b = ratAvg*((rect1[0]+rect1[2]/2) - (rect2[0]+rect2[2]/2))
	dis =  math.sqrt(a**2+ b**2)
	return dis

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#read image
image = cv2.imread("human1.jpg")
image = imutils.resize(image, width=min(800, image.shape[1]))
orig = image.copy()

# detect people in the image
(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
	padding=(8, 8), scale=1.05)

# draw the original bounding boxes
for (x, y, w, h) in rects:
	cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
print(rects)
print(pick)
# draw the final bounding boxes
for i in range(len(pick)):
	for j in range(len(pick)): #check
		xA , yA , xB , yB = pick[i][0] , pick[i][1] , pick[i][2] , pick[i][3]
		dis = caldist((xA,yA,xB-xA,yB-yA) , (pick[j][0] , pick[j][1] , pick[j][2] , pick[j][3]))
		if dis > FAR :
			cv2.line(image , (int((xA+xB)/2) , int((yA+yB)/2)) , (int((pick[j][0]+pick[j][2])/2) , int((pick[j][1]+pick[j][3])/2)) ,  
				(0, 255, 0), 2)
		else :
			cv2.line(image , (int((xA+xB)/2) , int((yA+yB)/2)) , (int((pick[j][0]+pick[j][2])/2) , int((pick[j][1]+pick[j][3])/2)) ,  
				(0, 0, 255), 2) 
		#print(dis)
		cv2.rectangle(image, (xA, yA), (xB, yB), (255, 255, 255), 2)
		cv2.circle(image,(int((xA+xB)/2) , int((yA+yB)/2) ),5,(255, 255, 255), -1)
	

cv2.imshow("Before NMS", orig)
cv2.imshow("After NMS", image)
cv2.waitKey(0)