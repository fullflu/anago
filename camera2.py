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



