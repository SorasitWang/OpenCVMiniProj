import numpy as np
import cv2
from collections import deque
from matplotlib import pyplot as plt
import utils as ut
from utils import MAX_INT

def recur(left,right,center,record,num,comp):
    global front,vertex,adja
    #for i in range(10):
   
    while(num > 0):
        #check whether left and right can connect
        t = ut.through(comp[left],comp[right],vertex,adja) #and through(left,center) and through(right,center)
        #print(left,center,right)
        #print(comp[left],comp[center],comp[right],t)
        if t :
            #reduce the piece that this component can produce
            num -= 1
            record = 0
            #add 
            front.append(comp[left]) ; front.append(comp[center]) ; front.append(comp[right])
            #move right to next vertex
            center = right
            right += 1
        elif record == 0 :
            right = center
            center = left
            left -= 1
            record += 1
        elif record == 1 :
           
            left = center
            for i in range(right,left) :
              
                if i != right and i != center and ut.through(comp[i],comp[left],vertex,adja) and ut.through(comp[i],comp[right],vertex,adja) and ut.through(comp[left],comp[right],vertex,adja):
                    #print(i)
                    front.append(comp[i]) ; front.append(comp[left]) ; front.append(comp[right])
                    recur(left,i+1,i,0,left-i-1,comp)
                    recur(i,right+1,right,0,i-right-1,comp)
                    return
def genEdge(v,offset):
    s = len(v)
    idx = []
    l1 = 0 ; l2 = 1; c = 0 ; r = 1
    for i in range(s):
        #print(l1,l2,c,r)
        idx.append(v[l1]) ; idx.append(v[c]+offset) ; idx.append(v[r])
        idx.append(v[(l2)%s]+offset) ; idx.append(v[c]+offset) ; idx.append(v[r])
        l1 += 1 ; l2 += 1 ; c += 1 ; r = (r+1)%s
        if (l2==2*s) : l2=s
    return idx



#vertex = [e for e in new]

edge = [[223, 1],[304 ,180],[394, 119],[313 ,305],[219 ,166],[108 ,272],[134, 182],[8 ,190],[13, 131],[180 ,93],[45 ,55]]
holeV = [[197,94],[247,94],[247,138],[197,138]]
vertex = edge + holeV

#adapt y-axis
for i in range(len(vertex)):
    vertex[i][1] = H - vertex[i][1]



#describe vertices that adjacent to it
adja = []
ut.genAdj(0,10,adja)
ut.genAdj(11,14,adja)
#Ex : [[10,1] , ...] mean vertex #10 and #1 adjacent with #0
#print(adja)

component = []
#seperate to many parts that no hole within
if (len(holeV)==0):
    component = [[i for i in range(len(vertex))]]
else :
    for i in range(len(holeV)):
        for j in range(len(edge)):
            #can connect
            if ut.through(j,len(edge)+i,vertex,adja) :
                adja[len(edge)+i].append(j)
                adja[j].append(len(edge)+i)
                break
        if i > 0 :
            e1 = adja[len(edge)+i-1][-1]
            e2 = adja[len(edge)+i][-1]
            tmpList = []
            tmpList.append(len(edge)+i) ; tmpList.append(len(edge)+i-1)
            for k in range(e1,e2+1):
                tmpList.append(k)
            component.append(tmpList)
    # the last part
    tmpList = []
    tmpList.append(len(edge)) ; tmpList.append(len(edge)+len(holeV)-1)
    for k in range(component[-1][-1],component[0][-1]+len(edge)+1):
        tmpList.append((k)%len(edge))
    component.append(tmpList)

#
front = []
#for generate 3D
edgeV = []

#recursive find the piece for each component
for i in range(len(component)):
    #left right centerb record num component
    recur(len(component[i])-1,1,0,0,len(component[i])-2,component[i])
    edgeV += [genEdge(component[i],len(vertex))]
    
'''print(front)
print(edgeV)
print(len(vertex))'''

#adapt y-axis back
for i in range(len(vertex)):
    vertex[i][1] = img.shape[0]-vertex[i][1]
#for draw piece
color = [0,0,0]
for i in range(0,len(front),3):
    color[int((i%9)/3)] = 255
    cv2.fillPoly(img, [np.array([vertex[front[i]],vertex[front[i+1]],vertex[front[i+2]]])], 
        color)
    color[int((i%9)/3)] = 0

#grouping piece
pieces = []
for i in range(len(front)-3):
    pieces += [[front[i],front[i+1],front[i+2]]]
print(pieces)

plt.imshow(img)
plt.show()
#[12, 13, 0, 1]


'''
recur(len(vertex)-1,1,0,0,len(vertex)-2)

for i in range(0,len(front),3):
    back.append(front[i]+len(vertex)) ; back.append(front[i+1]+len(vertex)) ; back.append(front[i+2]+len(vertex))
for i in range(len(vertex)):
    vertex1.append(vertex[i][0]/W) ; vertex1.append(vertex[i][1]/H) ; vertex1.append(0.0)
for i in range(len(vertex)):
    vertex2.append(vertex[i][0]/W) ; vertex2.append(vertex[i][1]/H) ; vertex2.append(-0.3)
edgeV = genEdge(len(vertex))
print(front)
print()
print(back)
print()
print(edgeV)
print()
print(vertex1)
print()
print(vertex2)
print()
print(len(front)+len(back)+len(edgeV))
plt.imshow(img)
plt.show()'''


