
import cv2
import matplotlib.pyplot as plt
import numpy as np

# 最简单的以灰度直方图作为相似比较的实现
def classify_gray_hist(image1,image2,size = (256,256)):
    # 先计算直方图
    # 几个参数必须用方括号括起来
    # 这里直接用灰度图计算直方图，所以是使用第一个通道，
    # 也可以进行通道分离后，得到多个通道的直方图
    # bins 取为16

    image1 = cv2.imread(image1)
    image2 = cv2.imread(image2)
    image1 = cv2.resize(image1,size)
    image2 = cv2.resize(image2,size)
    hist1 = cv2.calcHist([image1],[0],None,[256],[0.0,255.0])
    hist2 = cv2.calcHist([image2],[0],None,[256],[0.0,255.0])

    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i]-hist2[i])/max(hist1[i],hist2[i]))
        else:
            degree = degree + 1
    degree = degree/len(hist1)
    return degree

if __name__ == "__main__":
    ima1 = cv2.imread(r"screencapture - copy.bmp")
    ima2 = cv2.imread(r"screencapture.bmp")
    degree = classify_gray_hist(ima1, ima2)
    print(degree)