import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-qf", "--qualityfactor", help="Quality Factor of image", type=int)
parser.add_argument("-F", "--filename", help="name of file to pass in")

args = parser.parse_args()

rgb2yuv_mat = np.array(
    [[0.299, 0.587, 0.114], [-0.14713, -0.28886, 0.436], [0.615, -0.51499, -0.10001]])
yuv2rgb_mat = np.array(
    [[1, 0, 1.13983], [1, -0.39465, -0.58060], [1, 2.03211, 0]])

pi = math.pi
sqrt2 = math.sqrt(2)

LumaninanceQuantTable = np.array([[16, 11, 10, 16, 24, 40, 51, 61], [12, 12, 14, 19, 26, 58, 60, 55], [14, 13, 16, 24, 40, 57, 69, 56], [14, 17, 22, 29, 51, 87, 80, 62],
                                  [18, 22, 37, 56, 68, 109, 103, 77], [24, 35, 55, 64, 81, 104, 113, 92], [49, 64, 78, 87, 103, 121, 120, 101], [72, 92, 95, 98, 112, 100, 103, 99]])

ChrominanceQuantTable = np.array([[17, 18, 24, 47, 99, 99, 99, 99], [18, 21, 26, 66, 99, 99, 99, 99], [24, 26, 56, 99, 99, 99, 99, 99],
                                  [47, 66, 99, 99, 99, 99, 99, 99], [99, 99, 99, 99, 99, 99, 99, 99], [99, 99, 99, 99, 99, 99, 99, 99], [99, 99, 99, 99, 99, 99, 99, 99], [99, 99, 99, 99, 99, 99, 99, 99]])

DCTMat = 1/2*np.array([[1/sqrt2, 1/sqrt2, 1/sqrt2, 1/sqrt2, 1/sqrt2, 1/sqrt2, 1/sqrt2, 1/sqrt2],
                       [math.cos(pi/16), math.cos(3*pi/16), math.cos(5*pi/16), math.cos(7*pi/16), math.cos(
                           9*pi/16), math.cos(11*pi/16), math.cos(13*pi/16), math.cos(15*pi/16)],
                       [math.cos(2*pi/16), math.cos(6*pi/16), math.cos(10*pi/16), math.cos(14*pi/16),
                        math.cos(18*pi/16), math.cos(22*pi/16), math.cos(26*pi/16), math.cos(30*pi/16)],
                       [math.cos(3*pi/16), math.cos(9*pi/16), math.cos(15*pi/16), math.cos(21*pi/16),
                        math.cos(27*pi/16), math.cos(33*pi/16), math.cos(39*pi/16), math.cos(45*pi/16)],
                       [math.cos(4*pi/16), math.cos(12*pi/16), math.cos(20*pi/16), math.cos(28*pi/16),
                        math.cos(36*pi/16), math.cos(44*pi/16), math.cos(52*pi/16), math.cos(60*pi/16)],
                       [math.cos(5*pi/16), math.cos(15*pi/16), math.cos(25*pi/16), math.cos(35*pi/16),
                        math.cos(45*pi/16), math.cos(55*pi/16), math.cos(65*pi/16), math.cos(75*pi/16)],
                       [math.cos(6*pi/16), math.cos(18*pi/16), math.cos(30*pi/16), math.cos(42*pi/16),
                        math.cos(54*pi/16), math.cos(66*pi/16), math.cos(78*pi/16), math.cos(90*pi/16)],
                       [math.cos(7*pi/16), math.cos(21*pi/16), math.cos(35*pi/16), math.cos(49*pi/16), math.cos(63*pi/16), math.cos(77*pi/16), math.cos(91*pi/16), math.cos(105*pi/16)]])

DCTMatTranspose = np.transpose(DCTMat)

QualityFactor = args.qualityfactor
FileName = args.filename
#print(QualityFactor)
#print(FileName)

if QualityFactor < 50:
    ScaleFactor = 5000/QualityFactor
else:
    ScaleFactor = 200 - (QualityFactor*2)

ScaledLumaninanceTable = np.zeros((8,8))
ScaledChrominanceTable = np.zeros((8,8))

for i in range(8):
    for j in range(8):
        ScaledLumaninanceTable[i,j] = math.floor(((LumaninanceQuantTable[i,j] * ScaleFactor + 50) / 100))
        ScaledChrominanceTable[i,j] = math.floor(((ChrominanceQuantTable[i,j] * ScaleFactor + 50) / 100))
        if (ScaledLumaninanceTable[i,j] == 0):
            ScaledLumaninanceTable[i,j] = 1
        if (ScaledChrominanceTable[i,j] == 0):
            ScaledChrominanceTable[i,j] = 1
'''
print("This is the scaled lum table:")
print(ScaledLumaninanceTable)

print("This is the scaled chrom table:")
print(ScaledChrominanceTable)
'''

blocksize = 8

img = Image.open(FileName, 'r')
img = img.convert("RGB")
width, height = img.size

trimmedhratio = math.floor(height/blocksize)
trimmedwratio = math.floor(width/blocksize)

newheight = trimmedhratio * blocksize
newwidth = trimmedwratio * blocksize

img = img.resize((newwidth, newheight))
resize_img = np.array(img)

'''
print("This is the resized image in RGB before YUV conversion:")
plt.imshow(resize_img)
plt.show()
'''

yuv_img = np.zeros((newheight, newwidth, 3))
for i in range(newheight):
    for j in range(newwidth):
        yuv_img[i, j] = rgb2yuv_mat@resize_img[i, j]

Ychannel = yuv_img[:, :, 0]
Uchannel = yuv_img[:, :, 1]
Vchannel = yuv_img[:, :, 2]

# 4:2:0 Chromasubsampling
for r in range(0, newheight, 2):
    for c in range(0, newwidth, 4):
        USample1 = (Uchannel[r, c] + Uchannel[r, c + 1]) / 2
        # print("Uchannel[r, c]:", Uchannel[r, c], "Uchannel[r, c + 1]", Uchannel[r, c + 1], "USample1",  USample1)
        USample2 = (Uchannel[r, c + 2] + Uchannel[r, c + 3]) / 2
        VSample1 = (Vchannel[r, c] + Vchannel[r, c + 1]) / 2
        VSample2 = (Vchannel[r, c + 2] + Vchannel[r, c + 3]) / 2
        # print(type(USample1))
        # print(type(Uchannel[r, c]))
        Uchannel[r, c] = USample1
        Uchannel[r, c + 1] = USample1
        Uchannel[r + 1, c] = USample1
        Uchannel[r + 1, c + 1] = USample1
        Uchannel[r, c + 2] = USample2
        Uchannel[r, c + 3] = USample2
        Uchannel[r + 1, c + 2] = USample2
        Uchannel[r + 1, c + 3] = USample2
        Vchannel[r, c] = VSample1
        Vchannel[r, c + 1] = VSample1
        Vchannel[r + 1, c] = VSample1
        Vchannel[r + 1, c + 1] = VSample1
        Vchannel[r, c + 2] = VSample2
        Vchannel[r, c + 3] = VSample2
        Vchannel[r + 1, c + 2] = VSample2
        Vchannel[r + 1, c + 3] = VSample2

yuv_img[:, :, 1] = Uchannel
yuv_img[:, :, 2] = Vchannel

chromasampledYUV = np.array(yuv_img)

chromaRGB = np.zeros((newheight, newwidth, 3))
for i in range(newheight):
    for j in range(newwidth):
        chromaRGB[i, j] = yuv2rgb_mat@chromasampledYUV[i, j]
chromaRGB = (chromaRGB).astype(np.uint8)

'''
print("This is our chromasubsampled image:")
plt.imshow(chromaRGB)
plt.show()
'''

QuantMatrix = np.zeros((newheight, newwidth, 3))

for i in range(0, newheight, blocksize):
    r_index_start = i
    r_index_end = r_index_start + blocksize

    for j in range(0, newwidth, blocksize):
        c_index_start = j
        c_index_end = c_index_start + blocksize

        blockmatrixY = chromasampledYUV[r_index_start: r_index_end, c_index_start: c_index_end, 0]
        blockmatrixU = chromasampledYUV[r_index_start: r_index_end, c_index_start: c_index_end, 1]
        blockmatrixV = chromasampledYUV[r_index_start: r_index_end, c_index_start: c_index_end, 2]
        
        DCT2wayY = DCTMat@(blockmatrixY)@(DCTMatTranspose)
        DCT2wayU = DCTMat@(blockmatrixU)@(DCTMatTranspose)
        DCT2wayV = DCTMat@(blockmatrixV)@(DCTMatTranspose)

        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 0] = DCT2wayY
        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 0] = np.divide(QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 0], ScaledLumaninanceTable).astype(int)
        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 0] = np.multiply(QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 0], ScaledLumaninanceTable)
        
        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 1] = DCT2wayU
        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 1] = np.divide(QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 1], ScaledChrominanceTable).astype(int)
        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 1] = np.multiply(QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 1], ScaledChrominanceTable)

        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 2] = DCT2wayV
        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 2] = np.divide(QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 2], ScaledChrominanceTable).astype(int)
        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 2] = np.multiply(QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 2], ScaledChrominanceTable)

        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 0] = DCTMatTranspose@QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 0]@DCTMat
        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 1] = DCTMatTranspose@QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 1]@DCTMat
        QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 2] = DCTMatTranspose@QuantMatrix[r_index_start: r_index_end, c_index_start: c_index_end, 2]@DCTMat

rgbQuantMatrix = np.zeros((newheight, newwidth, 3))
for i in range(newheight):
    for j in range(newwidth):
        rgbQuantMatrix[i, j] = yuv2rgb_mat@QuantMatrix[i, j]

rgbQuantMatrix = (rgbQuantMatrix).astype(np.uint8)

'''
print("This is our chromasubsampled, compressed then reverted back to RGB:")
plt.imshow(rgbQuantMatrix)
plt.show()
'''

#ONE WAY TO SHOW THE 3 IMAGES SIDE BY SIDE BY TONS OF PIXELS THE SECOND FORM PUTS THEM INTO A CONDENSED SUBPLOT
Image.fromarray(np.hstack((resize_img,chromaRGB,rgbQuantMatrix))).show()

'''
f, axarr = plt.subplots(1,3)
axarr[0].imshow(resize_img)
axarr[1].imshow(chromaRGB)
axarr[2].imshow(rgbQuantMatrix)
plt.show()
'''