import numpy as np
import cv2
from collections import deque
from matplotlib import pyplot as plt



MAX_INT = 100000

def filterCont(contours,distance):
    new = np.array(contours[0][0][0])
    print(contours)
    for i in range(0,len(contours)):
        if ((contours[i][0][0] == new[-1][0])) : m = MAX_INT
        else : m = (contours[i][0][1]- new[-1][1]) / (contours[i][0][0] - new[-1][0])
        if (contours[(i+1)%len(contours)][0][0] == contours[i][0][0]) : mm = MAX_INT
        else : mm = (contours[(i+1)%len(contours)][0][1]- contours[i][0][1]) / (contours[(i+1)%len(contours)][0][0] - contours[i][0][0])
        if near(new[-1],contours[i][0],distance) or abs(mm-m) < 2 :
            pass
        else : 
            m = mm
            new = np.concatenate((new,[contours[i][0]]))
            tmp = contours[i][0]
#does 2 postion is near
def near(a,b,dis):
    if abs(a[0]-b[0]) + abs(a[1]-b[1]) <= dis :
        return True
    return False

#check intersect with : point line slope
def get_intersect2(a1,b1,b2,mA): 
    
    a1 = (p[0],p[1])
    a2 = (a[1][0] + mA,a[1][1] + mA)
   
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return False
    re = (x/z, y/z)
    return re
#generate adjacent list 
#Ex [[10,1] , ...] means vertex[0] adjacent with vertex[10] and vertex[1]
def genAdj(start,stop,adj):
    for i in range(start,stop+1):
        #print(adj)
        adj.append([])
        if i == start :
            adj[i].append( stop )
            adj[i].append( i+1 )
        elif i == stop :
            adj[i].append( i-1 )
            adj[i].append( start )
        else :
            adj[i].append( i-1 )
            adj[i].append( i+1 )

#does vertex[a] can darw through to vertex[b] according to adjacant list
def through(a,b,vertex,adja):
    #global vertex,adja
    maxX = max(vertex[a][0],vertex[b][0])
    minX = min(vertex[a][0],vertex[b][0])
    maxY = max(vertex[a][1],vertex[b][1])
    minY = min(vertex[a][1],vertex[b][1])
    if (vertex[a][0] - vertex[b][0] == 0) : slope = MAX_INT
    else : slope = ( vertex[a][1] - vertex[b][1] ) / ( vertex[a][0] - vertex[b][0] ) 
    c = vertex[b][1] - slope*vertex[b][0]
    for i in range(len(vertex)):
        if (i==a or i==b) : continue
        t = True
        #print(i,adja[i])
        for j in range(len(adja[i])):
            
            t = t and get_intersect(a,b,i,adja[i][j],vertex)
            if t :
                #print("1",i,j)
                return False
    return True
#line A1--A2 interset with B1--B2 or not
def get_intersect(A1, A2, B1, B2,vertex):
    a1 = (vertex[A1][0],vertex[A1][1])
    a2 = (vertex[A2][0],vertex[A2][1])
    b1 = (vertex[B1][0],vertex[B1][1])
    b2 = (vertex[B2][0],vertex[B2][1])
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return False
    re = (x/z, y/z)
    if re == a1 or re == a2 :
        
        return False
    if int(re[0]) not in range(min(a1[0],a2[0]),max(a1[0],a2[0])+1) or int(re[0]) not in range(min(b1[0],b2[0]),max(b1[0],b2[0])+1):
        
        return False
    if int(re[1]) not in range(min(a1[1],a2[1]),max(a1[1],a2[1])+1) or int(re[1]) not in range(min(b1[1],b2[1]),max(b1[1],b2[1])+1):
    
        return False
    return re
