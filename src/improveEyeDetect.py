import cv2
import numpy as np
from matplotlib import pyplot as plt
#For compare eyes size
CLOSEDSIZE  = 0.3
#Determine the eye is within the upper part of face or not
ABOVEFACE = 0.5

#For sorting
def myfunc(e) :
    return e[0]


def filteye(eyes,x,y,w,h):

    re = []
    #loop for candidate eye
    for i in range(len(eyes)):
        tmp = []
        #candidate eye is within the upper part of face?
        if eyes[i][1]+eyes[i][2]/2 < ABOVEFACE*h: 
            # find the pair
            for j in range(i,len(eyes)): 
                if eyes[j][1]+eyes[j][2]/2 < h*ABOVEFACE: 
                    #if they are close in size
                    if abs(eyes[i][2] - eyes[j][2]) <= CLOSEDSIZE*eyes[i][2] : 
                        #if overlap
                        if eyes[i][0] + eyes[i][2] >= eyes[j][0] and eyes[j][0] + eyes[j][2] >= eyes[i][0]:
                            continue
                        else:
                            #collect the different in y-axis and position  (float , [x,y]) for sorting
                            tmp.append( (abs(eyes[i][1]-eyes[j][1]),eyes[j]) ) 
            #if can't find the pair : find new candidate  
            if len(tmp) == 0 :
                continue
            if len(tmp) > 1:
                #sort by different in y-axis
                tmp.sort(key=myfunc)
            re.append(eyes[i])
            #choose the one that closet to the candiate
            re.append(tmp[0][1]) 
            return re
    return re

#import 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

#cap = cv2.VideoCapture(0)

while(1):
    # take each frame
    #_, frame = cap.read()
    #frame = cv2.flip(frame,1)

    #take from img file
    frame = cv2.imread("res/family.jpg")
    frameDup = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #detect face first
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        frameDup = cv2.rectangle(frameDup,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roiColor = frame[y:y+h, x:x+w]
        roiColorDup = frameDup[y:y+h, x:x+w]
        #detect eyes in face area
        eyes = eye_cascade.detectMultiScale(roi_gray)
        newEyes = filteye(eyes,x,y,w,h)
        #draw eyes border
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roiColor,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        for (ex,ey,ew,eh) in newEyes:
            cv2.rectangle(roiColorDup,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)    
    break

cv2.imshow('After',frameDup)
cv2.imshow('Before',frame)
cv2.waitKey(0)

