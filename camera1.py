#coding:utf-8

import cv2
import numpy as np

"""
必要そうなライブラリ -- raspberrypi

sudo apt-get install python-numpy
sudo apt-get install libopencv-dev
sudo apt-get install python-opencv

"""

"""
実行コマンド

python camera1

"""


# detect hands（これは保留）
def handdetect(im,mode):
    #when mode is 赤外線
    if mode == "seki":
        im_gray= cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        mask=im_gray >122
        im_bi = np.zeros((im_gray.shape[0],im_gray.shape[1]),np.uint8)
        im_bi[mask] = 255
        cv2.imshow("Binaryation",im_bi)
        #グレースケール変換後に2値変換
        #黒座標がFalse, 白座標がTrueで表された720×1200行列をmaskで返す
        return mask
        

    #色判定モード "color1" のとき．
    if mode=="color1":
        #画像全体から，b,g,r ごとに平均値を取得
        b,g,r = im.mean(0).mean(0) 
        print(r)#赤の値をprint
        cv2.imshow("camera",im)#frame出力
        #青が大きいとき，手が無いとしてFalseを返す（背景を青にしたとき）
        if b>170:
            return False
        else:
            return True
        
#手の場所を検出する（今のところの妥協案）
def handget(im,im_past,mode):
    #色判定モード "color2" のとき．雑な背景差分．
    if mode=="color2":
        #imとim_pastの差分を計算
        dif = im - im_past
        #difを全部の色で平均する（これで2次元配列になる）
        dif = dif.mean(axis=2)
        #差分が50（この50は適当なので要調整）より大きいところのindexを返す
        change_idx = np.where(dif>50)
        #差分が大きいところの平均座標をとって返す
        x = change_idx[0].mean()
        y = change_idx[1].mean()
        l2=[x,y]
        #cv2.imshow("camera",im)
        return l2

        
#iteration数
i=0

#前フレームのキャプチャ画像
im_past = None


while True:
    
    i+=1
    
    cap = cv2.VideoCapture(0)
    ret,im = cap.read()
    #capture missしたときはこれがprintされる
    if ret != True:
        print("capture miss!!")
    
    #print(im.shape) -> (720,1200,3)
    #キャプリャされた画像 im は，720×1200×3の3次元配列
    
    #l1=Trueなら手があったと判断 ---単純すぎるので保留
    #l1=handdetect(im,"color1")
    #print("l1=",l1)
    
    
    #手を追跡するなら，もう少し違うものが欲しい -> 変化があった場所の平均座標を返すhandget関数
    if im_past!= None:
        l2 = handget(im, im_past,"color2")
        print(l2)
        
    im_past = im.copy()
    
    k=cv2.waitKey(10)
    
    #Escキー押せばbreakできるはず．
    #なお自分のPCではできなかったので，iteration数でbreakしている
    if k==27 or i>50:
        break

#以下で開放してあげないと，"Camera dropped frame!"みたいになるので，つらい
cap.release()
cv2.destroyAllWindows() 


