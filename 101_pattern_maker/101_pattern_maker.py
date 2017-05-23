#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#モザイクのサイズが11から20までだった場合のためのパターン画像ファイルを生成。
#
#以下参考資料。
#  http://qiita.com/suto3/items/5181b4a3b9ebc206f579

from PIL import Image

def make_image(masksize, filename):
    picturesize = 2+masksize+masksize-1+2
    screen = (picturesize, picturesize)

    img = Image.new('RGB', screen, (0xff,0xff,0xff))

    pix = img.load()

    for i in range(2,picturesize,masksize-1):
        for j in range(2,picturesize,masksize-1):
            for k in range(0,picturesize):
                pix[i, k] = (0,0,0)
                pix[k, j] = (0,0,0)

    img.save(filename)
    return

for i in range(11, 20+1):
    make_image(i, "pattern"+str(i)+"x"+str(i)+".png")
