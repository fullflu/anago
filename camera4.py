#coding:utf-8

import cv2
import numpy as np
from math import *
import random
import time
import serial
from _socket import timeout

"""
---
import camera4
camera4.crun()

(break by control+C)

camera4.crush()
---
"""

def skinget(im_hsv):
    skin_min = np.array([0,58,89])
    skin_max = np.array([25,173,229])
    mask_skin = cv2.inRange(im_hsv,skin_min,skin_max)
    mask_skin = cv2.medianBlur(mask_skin,7)
    return mask_skin

def stickget(im_hsv):
    stick_min = np.array([95,0,20])
    stick_max = np.array([130,235,255])
    mask_stick = cv2.inRange(im_hsv,stick_min,stick_max)
    mask_stick = cv2.medianBlur(mask_stick,7)
    return mask_stick

#"/dev/tty.usbserial-AH02ERXN"


def seclose():
    #stop writing to arduino
    ser = serial.Serial("/dev/tty.usbmodem1421", 9600, timeout=1)
    ser.close()
    
    
def se2():
    #send serial message 0,30,60,...,270
    ser = serial.Serial("/dev/tty.usbmodem1421", 9600, timeout=1)
    for p in xrange(10):
        deg = p*30%360
        ser.write(str(deg)+'.')
        time.sleep(1)

def se():
    #send binary serial message 0,30,60,90
    ser = serial.Serial("/dev/tty.usbmodem1421", 9600, timeout=1)
    ser.bytesize = serial.EIGHTBITS
    for p in xrange(4):
        deg = p * 30
        print(ser.write(bin(p)))
        ser.write(bin(deg))
        print(bin(deg))
        time.sleep(1)

def get_deg(vec): 
    #get degree
    cos = (vec[0]*1)/(sqrt(vec[0]**2+vec[1]**2)+1)
    temp = acos(cos)
    deg = int(degrees(temp))
    if vec[1] < 0:
        deg = 360 - deg
    return deg

def crun(out=0):
    
    #mode -- 1 when spoken, 0 when not spoken
    mode = 0
    #iteration number
    j = 0
    #center of hand
    cx = 0
    cy = 0
    centr = (0,0)
    #center of stick
    cx2 = 0
    cy2 = 0    
    centr2 = (0,0)
    #ser = serial.Serial("/dev/tty.usbmodem1421",9600,timeout=1)
    
    while(1):
        j+=1
        #when j==1, we cannot get good image
        if j>2:
            #capture image from camera
            cap = cv2.VideoCapture(0)
            ret,im = cap.read()
            im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
            
            #crush the image window when out ==1
            if out == 1:
                cap.release()
                cv2.destroyAllWindows()
                break
            
            #get skin-color pixels and the image
            l = skinget(im_hsv)
            im_skin = cv2.bitwise_and(im_hsv,im_hsv, mask=l)
            
            #zero point of this camera system, visualized by a red point
            zeropoint = (700,500)
            cv2.circle(im_skin,zeropoint,5,[0,0,255],2)
            
            #get outline of hand
            contours,hierarchy = cv2.findContours(l,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            max_area = 0
            max_idx = 0
            #initialize contours area
            cnt = (0,0)
            for i in range(len(contours)):
                cnt = contours[i]
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    max_idx = i
                cnt = contours[max_idx]
                
            #get moment of hand
            moments = cv2.moments(cnt)
            if moments['m00']!=0:
                    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                    cy = int(moments['m01']/moments['m00']) # cy = M01/M00
                 
            #center of hand
            centr = (cx,cy)
            print(centr)
            #visualize center of hand by green circle
            cv2.circle(im_skin,centr,5,[0,255,0],2)
            
            if mode == 0:
                #get vector from zeropoint to center of hand
                vec = (centr[0] - zeropoint[0], centr[1] - zeropoint[1])
                deg = get_deg(vec)
                print(deg)
                #visualize line from zeropoint to center by green line
                cv2.line(im_skin,zeropoint,(zeropoint[0] + int(100*cos(radians(deg))),zeropoint[1] + int(100*sin(radians(deg)))),[0,255,0],2)
                #ser.write(str(deg)+'.')
                #a line above is to send serial message of hand direction
            
            if mode == 1:
                #get stick moment
                stick = stickget(im_hsv)
                contours2,hierarchy2 = cv2.findContours(stick,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                max_area2 = 0
                max_idx2 = 0
                cnt2 = (0,0)
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
                
                #get center of blue stick
                centr2 = (cx2,cy2)
                #visualize center of stick by blue circle
                cv2.circle(im_skin,centr2,5,[255,0,0],2)
                vec2 = (centr2[0]-centr[0] , centr2[1]-centr[1])
                deg = get_deg(vec2)
                #visualize vector from zeropoint to center of stick by blue line
                cv2.line(im_skin,zeropoint,(zeropoint[0] + int(100*cos(radians(deg))),zeropoint[1] + int(100*sin(radians(deg)))),[255,0,0],2)
                print(deg)
                #ser.write(str(deg)+'.')
                #a line above is to send serial message of stick direction           
            
            cv2.imshow("hand",im_skin)
            
            #speech mode is now randomized {0,1}
            mode = random.randint(0,1)
            
            k = cv2.waitKey(200)
            if k == 27:
                break
            
    cap.release()
    cv2.destroyAllWindows()
 
def crush():
    #crush the windows
    cv2.destroyAllWindows()
    
                
        
        
        
        
