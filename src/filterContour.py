import numpy as np
import cv2
from collections import deque
from matplotlib import pyplot as plt
import utils as ut
from utils import MAX_INT
import math


img = cv2.imread('res/table1.jpg')
H = img.shape[0] 
W = img.shape[1] 
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
#plt.imshow(img)
#plt.show()

#img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
#print(contours)

#holeV = contours[2]
#edge = contours[1]
#contours[1] =  np.concatenate((contours[1],contours[2]))


#pixel
offset = 2
print(len(contours))
for idx in range(len(contours)):

    tmp = contours[idx][0][0]
    new = np.array([tmp])

    print(new)
    new2 = np.array([tmp])

    for i in range(1,len(contours[idx])):
        if math.sqrt(pow(abs(contours[idx][i][0][0]-contours[idx][(i-1)%len(contours[idx])][0][0]),2) + pow(abs(contours[idx][i][0][1]-contours[1][(i-1)%len(contours[1])][0][1]),2) ) <= offset :
            #pass
            continue
        new = np.concatenate((new,[contours[idx][i][0]]))

    for i in range(len(new)):
        if new[i][0] == new2[-1][0] :
            m = MAX_INT
        else :
            m = (new[i][1] - new2[-1][1]) / (new[i][0] - new2[-1][0])  
        if new[i][1] > new2[-1][1] and (new[i][0] > new2[-1][0]) :    mQ = 1
        elif new[i][0] > new2[-1][0] :   mQ = 4
        elif new[i][1] < new2[-1][1] and (new[i][0] < new2[-1][0]):   mQ = 3 
        else : mQ = 2

        if new[(i+1)%len(new)][0] == new[i][0] :
            mm = MAX_INT
        else :
            mm = ( new[(i+1)%len(new)][1] - new[i][1] ) / (new[(i+1)%len(new)][0] - new[i][0] )  


        if  new[(i+1)%len(new)][1] > new[i][1] and ( new[(i+1)%len(new)][0] > new[i][0]) :    mmQ = 1
        elif  new[(i+1)%len(new)][0] > new[i][0] :   mmQ = 4
        elif  new[(i+1)%len(new)][1] < new[i][1] and ( new[(i+1)%len(new)][0] < new[i][0]):   mmQ = 3 
        else : mmQ = 2

        if abs(m-mm) < 2 and (mQ==mmQ) :
            continue
        else :
            #plt.plot(new[i][0],H-new[i][1],'bo', linewidth=1)
            #img = cv2.circle(img, (new[i][0],new[i][1]), 5, (255,0,0), 5)
            new2 = np.concatenate((new2,[new[i]]))
        
    #print(contours)
    #print(new2)
    img = cv2.drawContours(img, [new2], -1, (255,0,0), 3)
    #plt.imshow(img)
    #plt.show()
    print("The Number of contour ",idx," before filted : ",len(contours[idx]))
    print("The Number of contour ",idx," after filted : ",len(new2))
plt.imshow(img)
plt.show()