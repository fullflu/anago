#coding:utf-8

import cv2
import numpy as np
from math import *
import random

import serial
from _socket import timeout

"""
---
import camera4
camera4.run()

(break by control+C)

camera4.crush()
---
"""

def skinget(im_hsv):
    skin_min = np.array([0,58,89])
    skin_max = np.array([25,173,229])
    
    mask_skin = cv2.inRange(im_hsv,skin_min,skin_max)
    mask_skin = cv2.medianBlur(mask_skin,7)
    #print(mask_skin)
    #im_skin = cv2.bitwise_and(im_hsv,im_hsv, mask=mask_skin)
    #cv2.imshow("skin",im_skin)
    return mask_skin

def stickget(im_hsv):
    stick_min = np.array([95,0,20])
    stick_max = np.array([130,235,255])
    
    mask_stick = cv2.inRange(im_hsv,stick_min,stick_max)
    mask_stick = cv2.medianBlur(mask_stick,7)
    
    return mask_stick

#this does not work well
#"/dev/tty.usbserial-AH02ERXN"
def se():
    ser = serial.Serial("/dev/tty.usbmodem1421",9600,timeout=1)
    for i in xrange(5):
        flag=i*30
        #str(i)+
        ser.write(str(flag)+'\0')
    ser.close()


def crun(out=0):
    
        
    mode=0
    sp=0
    j=0
    
    cx=0
    cy=0
    cx2=0
    cy2=0
    centr=(0,0)
    centr2=(0,0)
    
    ser = serial.Serial("/dev/tty.usbmodem1421",9600,timeout=1)
    
    
    while(1):
        j+=1
        
        if j>2:
    
            #capture image from camera
            cap = cv2.VideoCapture(0)
            ret,im = cap.read()
            im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
            
            zeropoint = (im[0].mean(),im[1].mean())
            
            if out==1:
                cap.release()
                cv2.destroyAllWindows()
                break
            
            
            #get skin-color pixels
            l=skinget(im_hsv)
            im_skin = cv2.bitwise_and(im_hsv,im_hsv, mask=l)
            
            
            #get outline of hand
            contours,hierarchy = cv2.findContours(l,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
            max_area = 0
            max_idx = 0
            cnt=(0,0)
            for i in range(len(contours)):
                cnt = contours[i]
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    max_idx = i
                    
                cnt = contours[max_idx]
            
            
            moments = cv2.moments(cnt)
            if moments['m00']!=0:
                    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                    cy = int(moments['m01']/moments['m00']) # cy = M01/M00
                  
            #center of hand
            centr=(cx,cy)
            #visualize center of hand by blue circle
            cv2.circle(im_skin,centr,5,[0,0,255],2)
            
            
            if mode==0:
                print(centr)
                flag = 60
                ser.write(flag)
            
            mode = 1#sp
            
            if mode ==1:
                stick = stickget(im_hsv)
                im_stick = cv2.bitwise_and(im_hsv,im_hsv, mask=stick)
            
            
            #get outline of hand
                contours2,hierarchy2 = cv2.findContours(stick,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                
                max_area2 = 0
                max_idx2 = 0
                cnt2=(0,0)
                for i in range(len(contours2)):
                    cnt2 = contours2[i]
                    area2 = cv2.contourArea(cnt2)
                    if area2 > max_area2:
                        max_area2 = area2
                        max_idx2 = i
                        
                    cnt2 = contours2[max_idx2]
                
                
                moments = cv2.moments(cnt2)
                if moments['m00']!=0:
                        cx2 = int(moments['m10']/moments['m00']) # cx = M10/M00
                        cy2 = int(moments['m01']/moments['m00']) # cy = M01/M00
                      
                #center of hand
                centr2=(cx2,cy2)
                #visualize center of hand by blue circle
                cv2.circle(im_skin,centr2,5,[255,0,0],2)
                
                
            
            #get hand direction when mode==1 (when someone speaks to microphone)
            if mode==2:
                try:
                    hull = cv2.convexHull(cnt,returnPoints = False)
                except:
                    mode=0
                    print("hull")
                    continue
                 
                    
                try:
                    defects = cv2.convexityDefects(cnt,hull)
                except:
                    mode=0
                    print("defects")
                    continue
                
                if defects ==None:
                    mode=0
                    continue
                
                
                a0=[0,0]
                min_cos=0
                yubi=(0,0)
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
                cv2.circle(im_skin,yubi,5,[255,0,0],2)
                
                #direction to which finger direct
                vec = (yubi[0]-centr[0], yubi[1]-centr[1])
                
                #visualize the vec as blue line
                cv2.line(im_skin,centr,yubi,[255,0,0],2)
            
            cv2.imshow("hand",im_skin)
            
            
            #speech mode is now randomized
            sp=random.randint(0,1)
            
            k=cv2.waitKey(200)
            if k ==27:
                break
        
        
    cap.release()
    cv2.destroyAllWindows()
        


 
def crush():
    #crush the windows
    cv2.destroyAllWindows()
    
                
        
        
        
        
