#coding:utf-8

import cv2
import numpy as np

#git clone https://github.com/fullflu/anago

"""
..install library (Linux)

sudo apt-get install python-numpy
sudo apt-get install libopencv-dev
sudo apt-get install python-opencv

"""

"""
..command

python camera2.py

"""

#detect skin
def skinget(im_hsv):
    skin_mini = np.array([0,58,89])
    skin_max = np.array([25,173,229])
    
    mask_skin = cv2.inRange(im_hsv,skin_mini,skin_max)
    mask_skin = cv2.medianBlur(mask_skin,7)
    
    im_skin = cv2.bitwise_and(im_hsv,im_hsv, mask=mask_skin)
    cv2.imshow("skin",im_skin)
    return mask_skin


i=0

while True:
    
    #iterarion count to break
    i+=1
    
    #capture image from camera
    cap = cv2.VideoCapture(0)
    ret,im = cap.read()
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    
    #get skin-color pixels
    l=skinget(im_hsv)
    change_idx = np.where(l>0)
    
    #median of skin-color pixels
    x = np.median(change_idx[0])
    y = np.median(change_idx[1])
    skin_median= [x,y]
    print(skin_median)
    
    k=cv2.waitKey(100)

    if i > 50:
        break
    
cap.release()
cv2.destroyAllWindows()


def convex_defects(mode,cnt,centr,im_skin):
# get convexhull and convexdefects (usually we don't use this)
    if mode == 2:
        try:
            hull = cv2.convexHull(cnt,returnPoints = False)
        except:
            mode=0
            print("hull")
            #break
            
        try:
            defects = cv2.convexityDefects(cnt,hull)
        except:
            mode=0
            print("defects")
            #break
        
        if defects ==None:
            mode=0
            #break
        
        a0 = [0,0]
        min_cos = 0
        yubi = (0,0)
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            #dist = cv2.pointPolygonTest(cnt,centr,True)
            
            #visualize hand outline by green line
            cv2.line(im_skin,start,end,[0,255,0],2) 
            #visualize hand corner by red circle
            cv2.circle(im_skin,far,5,[0,0,255],-1)
            
            a1 = [start[0]-end[0],start[1]-end[1]]
            #get cosine
            cos = (a1[0]*a0[0]+a1[1]*a0[0])/(sqrt(a1[0]**2+a1[1]**2)+sqrt(a0[0]**2+a0[1]**2))
            if cos < min_cos:
                min_cos = cos
                yubi = start
            a0 = a1
        
        #visualize the tip of finger circle
        #cv2.circle(im_skin,yubi,5,[255,0,0],2)
        
        #direction to which finger direct
        vec = (yubi[0]-centr[0], yubi[1]-centr[1])
    return vec
        #visualize the vec as blue line
        #cv2.line(im_skin,centr,yubi,[255,0,0],2)
