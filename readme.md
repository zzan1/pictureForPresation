# Basic Intro

这个项目的最初想法来源于: 讲座或者有些课程老师的 slide 文件不会分享，自己在认真听讲的同时，一边要思考，一边还要忙着去截屏，保存图片。这个痛处决定了这个项目的诞生。

你可以利用这个项目：选择截取的屏幕，自动存储不相同的 slide 图片。

# Todo list

- [ ] 优化图像识别，尝试更多的图像识别方式，可以做一个收集整理。
- [ ] 设置触发按钮，现阶段是定时截屏，可以做一个触发截屏。
- [ ] 编写图形化界面，增加自动选择程序，增加发送图片的程序。
- [ ] 规范化代码编写

# Tips in the procedure

写一个知识点列表，帮助自己回忆学到的知识点，并且企图更好的在重复的过程中能有新的突破。

## get the screenshot

> [How to fast get a screenshot in windows](https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows) 

```python
import win32gui
import win32ui 
hwnd = win32gui.FindWindow(None, windowname)
wDC = win32gui.GetWindowDC(hwnd)
dcObj=win32ui.CreateDCFromHandle(wDC)
cDC=dcObj.CreateCompatibleDC()
dataBitMap = win32ui.CreateBitmap()
dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
cDC.SelectObject(dataBitMap)
cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
# Free Resources
dcObj.DeleteDC()
cDC.DeleteDC()
win32gui.ReleaseDC(hwnd, wDC)
win32gui.DeleteObject(dataBitMap.GetHandle())
```
- [ ] 代码一句句的解释

## figure classify 
 
[Python+Opencv进行识别相似图片](https://blog.csdn.net/feimengjuan/article/details/51279629) 

选取了最为简单了**灰度直方图** 来实现不同图片的识别。

```python
import cv2
import numpy as np
from matplotlib import pyplot as plt
 
# 最简单的以灰度直方图作为相似比较的实现
def classify_gray_hist(image1,image2,size = (256,256)):
    # 先计算直方图
    # 几个参数必须用方括号括起来
    # 这里直接用灰度图计算直方图，所以是使用第一个通道，
    # 也可以进行通道分离后，得到多个通道的直方图
    # bins 取为16
    image1 = cv2.resize(image1,size)
    image2 = cv2.resize(image2,size)
    hist1 = cv2.calcHist([image1],[0],None,[256],[0.0,255.0])
    hist2 = cv2.calcHist([image2],[0],None,[256],[0.0,255.0])
    # 可以比较下直方图
    plt.plot(range(256),hist1,'r')
    plt.plot(range(256),hist2,'b')
    plt.show()
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i]-hist2[i])/max(hist1[i],hist2[i]))
        else:
            degree = degree + 1
    degree = degree/len(hist1)
    return degree
```

# clipboard and Handle of bitmap

利用 `pywin32` 把图片放入 clipboard 中，参考了：
[clipboard](https://blog.csdn.net/tcjiaan/article/details/8712276) 

主要是学习了利用 `pywin32` 访问剪贴板的操作。
```python
def setImageInClip(data):
    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(win32con.CF_BITMAP,data)
    clip.CloseClipboard()
```

查阅 windows 关于剪贴板格式的文档，得知 `CF_BITMAP` 就是处理 `Handle bitmap` 格式的。所以可以直接利用 `setImageInClip(dataBitMap.GetHandle())` 直接将截图数据传输到剪贴板中。 
