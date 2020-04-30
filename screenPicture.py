import win32gui
import win32ui
import win32con
import win32clipboard as clip
import cv2, numpy

def getTheScreenshot(picName, width=1430, height=991):
    hwnd = win32gui.FindWindow('VideoContainerWndClass', 'VideoContainerWnd')  #窗口的类名可以用Visual Studio的SPY++工具获取
    # hwnd = win32gui.GetDesktopWindow()
    # print("%x" % hwnd)

    #获取句柄窗口的大小信息
    # left, top, right, bot = win32gui.GetWindowRect(hwnd)
    # print(left,top, right, bot)
    # width = right - left
    # height = bot - top
    # print(width, height)
    width = width
    height = height
    # returns the device context (DC) for the entire window, including title bar, menus, and scroll bars.
    # 设备描述表是一个定义一组图形对象及其属性、影响输出的图形方式(数据)结构。windows提供设备描述表，用于应用程序和物理设备之间进行交互，从而提供了应用程序设计的平台无关性。设备描述表又称为设备上下文，或者设备环境。
    # windows 窗口一旦创建，它就自动地产生了与之相对应的设备描述表数据结构，用户可运用该结构，实现对窗口显示区域的GDI操作，如划线、写文本、绘制位图、填充等，并且所有这些操作均要通过设备描述表句柄来进行。
    wDC = win32gui.GetWindowDC(hwnd)
    dcObject = win32ui.CreateDCFromHandle(wDC)
    # Creates a memory device context (DC) compatible with the specified device.
    # 创建一个和指定设备上下文兼容的存储设备上下文
    cDC = dcObject.CreateCompatibleDC()
    # 创建一个位图对象
    dataBitMap = win32ui.CreateBitmap()
    #  创建一个和设备颜色格式兼容的画布
    dataBitMap.CreateCompatibleBitmap(dcObject, width, height)
    # Selects an object into the specified device context (DC). The new object replaces the previous object of the same type.
    cDC.SelectObject(dataBitMap)
    # Performs a bit-block transfer of the color data corresponding to a rectangle of pixels from the specified source device context into a destination device context.
    cDC.BitBlt((0, 0), (width, height), dcObject, (0, 0), win32con.SRCCOPY)
    # dataBitMap.SaveBitmapFile(cDC,screenImage)
    # dataBitMap.GetHandle() 可以直接扔到剪贴板里面

    # 保存图片
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    im_opencv = numpy.frombuffer(signedIntsArray, dtype = 'uint8')
    im_opencv.shape = (height, width, 4)
    cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)

    cv2.imwrite(picName ,im_opencv,[int(cv2.IMWRITE_JPEG_QUALITY), 100]) #保存

   
    # setImageInClip(dataBitMap.GetHandle())

    # Free Resources
    dcObject.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())


def setImageInClip(data):
    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(win32con.CF_BITMAP,data)
    clip.CloseClipboard()

if __name__ == "__main__":
    getTheScreenshot('picname')
    