import classifyImage
import screenPicture
import time, datetime
import os

if __name__ == "__main__":
    i = 1
    temp_name = 'picLib\\temp.jpg'
    normal_name = 'picLib\\' + str(i) + '.jpg'
    while True:
        with open('log.txt', 'a+') as f:
            if i == 1:
                # 直接把第一张图片存入
                screenPicture.getTheScreenshot(normal_name)
                now = datetime.datetime.ctime(datetime.datetime.now())
                f.write(now + " 写入第" + str(i) + "张图片!\n")
                i = i + 1

            # 休息20s，得到第二张图
            time.sleep(20)
            screenPicture.getTheScreenshot(temp_name)

            # 比较这两张图
            degree = classifyImage.classify_gray_hist(normal_name, temp_name)

            # 排除当图片完全相等的时候，返回的值 是 1.0 会出错的情况。
            if degree == 1.0:
                degree = [1.0]

            # 两张图片差距大的时候,把 temp 这个图片名字改为 正常图片
            if degree[0] < 0.7:
                normal_name = 'win32gui\\test\\' + str(i) + '.jpg'
                now = datetime.datetime.ctime(datetime.datetime.now())
                os.rename(temp_name, normal_name)
                f.write(now + " 写入第 " + str(i) + " 张图片!\n")
                i = i + 1

            else:
                now = datetime.datetime.ctime(datetime.datetime.now())
                f.write(now + " 图片相同\n")
