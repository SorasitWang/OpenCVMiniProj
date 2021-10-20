import cv2
import numpy as np
from matplotlib import pyplot as plt

CLOSEDSIZE  = 0.3
ABOVEFACE = 0.5
def myfunc(e) :
    return e[0]
def filteye(eyes,x,y,w,h):
    # if len(eyes) <= 2 :
    #     return eyes
    re = []
    for i in range(len(eyes)):
        tmp = []
        if eyes[i][1]+eyes[i][2]/2 < ABOVEFACE*h: #ตาอยู่ส่วนบนของหน้า
            for j in range(i,len(eyes)):
                if eyes[j][1]+eyes[j][2]/2 < h*ABOVEFACE:
                    if abs(eyes[i][2] - eyes[j][2]) <= CLOSEDSIZE*eyes[i][2] : #ขนาดใกล้กัน
                        if eyes[i][0] + eyes[i][2] >= eyes[j][0] and eyes[j][0] + eyes[j][2] >= eyes[i][0]: #ทับซ้อนกัน
                            continue
                        else:
                            tmp.append( (abs(eyes[i][1]-eyes[j][1]),eyes[j]) ) #สำหรับ sort ตามความต่างของแกนy
                   
            if len(tmp) == 0 :
                continue
            if len(tmp) > 1:
                tmp.sort(key=myfunc)
            re.append(eyes[i])
            re.append(tmp[0][1]) 
            return re
    return re


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#cap = cv2.VideoCapture(0)
while(1):
    # Take each frame
    #_, frame = cap.read()
    #frame = cv2.flip(frame,1)
    frame = cv2.imread("nick_test1.jpg")
    #frame = cv2.resize(frame,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        #eyes = filteye(eyes,x,y,w,h)
        
        if len(eyes) != 0 :
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',frame)
    break
   
cv2.imshow('img',frame)
cv2.waitKey(0)

