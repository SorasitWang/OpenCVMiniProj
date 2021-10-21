from __future__ import print_function
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

class Window :

    def __init__(self):
        self.draw = True
        self.penSize = 3
        self.color = (255,255,255)
        self.menuSize = (640,70)
        
    def setup(self,tab):
        tab = cv2.rectangle(tab,(0,0),self.menuSize,(255,255,255),-1)
        #color
        cv2.circle(tab,(32,35),32,(0,255,0),-1)
        cv2.circle(tab,(96,35),32,(255,0,0),-1)
        cv2.circle(tab,(160,35),32,(0,0,255),-1)
        cv2.circle(tab,(224,35),32,(0,0,0),-1)
        cv2.circle(tab,(288,35),32,(240,240,240),-1)
        #size
        cv2.rectangle(tab,(330,3),(500,68),(200,200,200),-1)
        cv2.rectangle(tab,(330,21),(500,50),(150,150,150),-1)
        cv2.circle(tab,((self.penSize*17)+325,35),5,(0,0,0))
        cv2.putText(tab,"size ="+str(self.penSize),(510,35),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,150,255),2)

        cv2.putText(tab,str("Draw" if self.draw else "Edit"),(600,35),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,150,255),2)
    
    
    def run(self,res,point,oldPoint,k):
        
        #self.setup(tab)
        #escape => change mode
        
        if k == ord('m'):
            print("change")
            self.draw = not self.draw
        if self.draw and point[1] < 70 :
            print(point[0])
            if (point[0] < 320):
                self.changeColor(point[0])
            else :
                self.changeSize(point[0])
        elif not mode:
            res = cv2.line(res,oldPoint,point, self.color, self.penSize)
        return res

    def changeSize(self,x):
        if (x>=330 and x<=500):
            self.penSize = int((x-330)/17)+1
       
    def changeMode(self):
        self.draw = not self.draw
    
    def changeColor(self,x):
        
        if (x<64):
            self.color = (0,255,0)
        elif (x<128) :
            self.color = (255,0,0)
        elif (x<192):
            self.color = (0,0,255)
        elif (x<256):
            self.color = (0,0,0)
        else :
            self.color = (255,255,255)
        
    
    


#set shape
cap = cv2.VideoCapture(0)
_, frame = cap.read()
res = np.zeros(frame.shape,np.uint8) 
#set var
mode = False
size = 3
oldPoint = ()

window = Window()
while(1):
    # Take each frame
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    frameDup = frame.copy()
    window.setup(frameDup)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #define detected color
    lower_green= np.array([110,105,30])
    upper_green = np.array([140,130,80])
    mask = cv2.inRange(frame, lower_green, upper_green)

    cnt, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #if dectect
    k = cv2.waitKey(5) & 0xFF

    if (len(cnt)!=0):
        c = max(cnt, key = cv2.contourArea)
        leftmost = (tuple(c[c[:,:,0].argmin()][0]))
        rightmost = (tuple(c[c[:,:,0].argmax()][0]))
        topmost = (tuple(c[c[:,:,1].argmin()][0]))
        bottommost = (tuple(c[c[:,:,1].argmax()][0]))

        #define the track point
        #point = ( int((rightmost[0]+leftmost[0])/2) , int((topmost[1]+bottommost[1])/2) )
        point = leftmost
        if (oldPoint == ()):
            oldPoint = point
        #print(oldPoint)
        #print(point)
        res = window.run(res,point,oldPoint,k)
        oldPoint = point
        
    cv2.imshow('frame',frameDup)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    #k = cv2.waitKey(5) & 0xFF
    #quit
    if k == ord('q'):
        break
    #clearq
    elif k == ord('c'):
        res = np.zeros(frame.shape,np.uint8) 

cv2.destroyAllWindows()