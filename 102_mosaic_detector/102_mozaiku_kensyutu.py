#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#モザイクの箇所を検出し、白塗りする。
#以下参考資料。
#  ・Template Matching
#    http://docs.opencv.org/3.2.0/d4/dc6/tutorial_py_template_matching.html
#    http://opencv.jp/cookbook/opencv_img.html#id32


import cv2
import numpy as np
from PIL import Image

import sys
args = sys.argv

def make_image(masksize):
    picturesize = 2+masksize+masksize-1+2
    screen = (picturesize, picturesize)

    img = Image.new('RGB', screen, (0xff,0xff,0xff))

    pix = img.load()

    for i in range(2,picturesize,masksize-1):
        for j in range(2,picturesize,masksize-1):
            for k in range(0,picturesize):
                pix[i, k] = (0,0,0)
                pix[k, j] = (0,0,0)
    return img
    
if len(args) != 2:
    print("too few argument.")
    sys.exit(1)

img_rgb = cv2.imread(args[1])

img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) #グレースケールに
img_gray = cv2.Canny(img_gray,10,20) #エッジ検出
img_gray = 255-img_gray #白黒反転
img_gray = cv2.GaussianBlur(img_gray,(3,3),0) #少しぼかす

cv2.imwrite('output_gray.png', img_gray)

for i in range(11,20+1):
    image_array = np.array(make_image(i))
    template = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]

    img_kensyutu_kekka = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.3
    loc = np.where(img_kensyutu_kekka >= threshold)
    for pt in zip(*loc[::-1]):
        #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255,255,255), 1)
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255,255,255), -1)
    cv2.imwrite('output_progress_'+str(i)+'.png', img_rgb)

cv2.imwrite('output_result.png', img_rgb)

cv2.imshow('window1', img_rgb)
cv2.imshow('window2', img_gray)
cv2.waitKey(0)

cv2.destroyAllWindows()
