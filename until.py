import json
import mss
import pyautogui
import requests
import win32api
import wmi


# python接受
# 登陆成功0 没有卡返回1 超过两台设备2 过期返回3
# 后端返回
# 没有卡返回1 有卡未激活返回2 有卡是一台设备返回没过期3 有卡不是一台设备返回4 有卡是一台设备但是过期返回5

def denglu(card, jiqima):
    post_dict = {'card': card, 'jiqima': jiqima}
    a = requests.post("http://120.46.214.147:8088/thunderwarocean/user/yanzheng", post_dict)
    state = json.loads(a.text)
    # print(state)
    if state['code'] == "1":
        # print("登录返回1")
        return 1
    if state['code'] == "2":
        # print("登录返回2")
        return 0
    if state['code'] == "3":
        # print("登录返回3")
        return 0
    if state['code'] == "4":
        # print("登录返回4")
        return 2
    if state['code'] == "5":
        # print("登录返回5")
        return 3


def locate(p, m):
    sec = mss.mss()
    zone = {
        'left': 0,  # 2112
        'top': 0,  # 995
        'width': 1920,  # 2550
        'height': 1080  # 1435
    }

    bg = sec.grab(zone)
    bg1 = np.array(bg)
    img = cv2.imread(p, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 根据像素的范围进行过滤，把符合像素范围的保留，不符合的赋值0或者255
    # 根据hsv颜色表找出最大值和最小值
    mask = cv2.inRange(hsv, (35, 43, 46), (77, 255, 255))
    mask = cv2.bitwise_not(mask)
    result = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow('1',result)
    # cv2.waitKey(2000)
    # cv2.destroyAllWindows()
    # 读取背景图片和缺口图片
    # bg = cv2.imread('map.png')  # 背景图片
    # tp_img = cv2.imread(tp)  # 缺口图片

    # 识别图片边缘
    # bg_edge = cv2.Canny(bg, 100, 200)
    # tp_edge = cv2.Canny(result, 100, 200)

    # 转换图片格式
    bg_pic = cv2.cvtColor(bg1, cv2.COLOR_BGR2BGRA)
    tp_pic = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    # cv2.imshow('1',bg_pic)
    # cv2.waitKey(5000)
    # cv2.destroyAllWindows()
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    if max_val < m:
        # print((-114514,-114514))
        return None
    else:
        th, tw = result.shape[:2]
        tl = max_loc  # 左上角点的坐标
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
        b = cv2.rectangle(bg1, tl, br, (0, 0, 255), 2)
        x, y = (tl[0] + br[0]) / 2, (tl[1] + br[1]) / 2
        a = (int(x), int(y))
        return a


def click(p):  # 第二种
    x = p[0]
    y = p[1]
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    pyautogui.moveTo(x=20, y=300)


def mouseMove(x, y):
    win32api.SetCursorPos((x, y))


def get_baseboard_sn():
    """
    获取主板序列号
    :return: 主板序列号
    """
    c = wmi.WMI()
    for board_id in c.Win32_BaseBoard():
        # print(board_id.SerialNumber)
        return board_id.SerialNumber


def detect_green_circle():
    bbox = (508, 347, 1371, 807)  # 截图区域的边界框
    # 904,610
    screenshot = np.array(ImageGrab.grab(bbox=bbox))
    # 将BGR格式的图像转换为HSV格式
    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
    # 定义绿色范围
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])
    # 提取绿色区域
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # 霍夫圆变换
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    # 如果检测到圆，则返回圆心坐标
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        return (circles[0][0], circles[0][1])
    # 如果没有检测到圆，则返回None
    else:
        return None


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


import sys
import os


# def get_resource_path1(relative_path):
#     """获取资源文件的绝对路径"""
#     try:
#         # PyInstaller会设置sys._MEIPASS，用于访问临时目录中的文件
#         base_path = sys._MEIPASS
#     except Exception:
#         # 如果没有设置sys._MEIPASS，则使用当前工作目录作为基础路径
#         base_path = os.path.abspath(".")
#
#     # 返回相对路径所对应的文件的绝对路径
#     return os.path.join(base_path, relative_path)


def get_cpu_sn():
    """
    获取CPU序列号
    :return: CPU序列号
    """
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        # print(cpu.ProcessorId.strip())
        return cpu.ProcessorId.strip()


def findjiantoulvse(a, b, c, d):
    from PIL import ImageGrab

    # 指定查找的屏幕区域
    bbox = (a, b, c, d)
    # bbox = (414, 384, 877, 386)720p

    # 截屏并获取像素数据
    screenshot = ImageGrab.grab()
    pixel_data = screenshot.load()

    # 遍历第 475 行像素，查找绿色像素
    for x in range(bbox[0], bbox[2]):
        pixel_color = pixel_data[x, bbox[1]]
        if pixel_color[0] < 100 and pixel_color[1] > 200 and pixel_color[2] < 100:  # 判断像素是否绿色
            return x


def findjiantouhongse(a, b, c, d):
    from PIL import ImageGrab

    # 指定查找的屏幕区域
    # bbox = (414, 384, 877, 386)720p
    bbox = (a, b, c, d)

    # 截屏并获取像素数据
    screenshot = ImageGrab.grab()
    pixel_data = screenshot.load()

    # 遍历第 475 行像素，查找绿色像素
    for x in range(bbox[0], bbox[2]):
        pixel_color = pixel_data[x, bbox[1]]
        if pixel_color[0] > 200 and pixel_color[1] < 150 and pixel_color[2] < 150:  # 判断像素是否绿色
            return x


def findheise(x1, y1, x2, y2):
    import numpy as np
    from mss import mss
    import cv2
    with mss() as sct:
        # 获取指定区域的屏幕截图
        monitor = {"left": x1, "top": y1, "width": x2 - x1, "height": y2 - y1}
        img = np.array(sct.grab(monitor))

    # 将 BGR 转为 RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 在指定的 RGB 范围内查找黑色像素点
    mask = cv2.inRange(img, (0, 0, 0), (0, 0, 0))

    # 判断是否存在红色像素点
    if cv2.countNonZero(mask) > 0:
        # print("1")
        return True
    else:
        # print("2")
        return False


def findheise2(x1, y1, x2, y2):
    import numpy as np
    from mss import mss
    import cv2
    with mss() as sct:
        # 获取指定区域的屏幕截图
        monitor = {"left": x1, "top": y1, "width": x2 - x1, "height": y2 - y1}
        img = np.array(sct.grab(monitor))

    # 将 BGR 转为 RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 在指定的 RGB 范围内查找黑色像素点
    mask = cv2.inRange(img, (0, 0, 0), (40, 40, 40))

    # 判断是否存在红色像素点
    if cv2.countNonZero(mask) > 0:
        # print("1")
        return True
    else:
        # print("2")
        return False


def findhongse(x1, y1, x2, y2):
    import numpy as np
    from mss import mss
    import cv2
    with mss() as sct:
        # 获取指定区域的屏幕截图
        monitor = {"left": x1, "top": y1, "width": x2 - x1, "height": y2 - y1}
        img = np.array(sct.grab(monitor))

    # 将 BGR 转为 RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 在指定的 RGB 范围内查找红色像素点
    mask = cv2.inRange(img, (220, 0, 0), (255, 30, 30))

    # 判断是否存在红色像素点
    if cv2.countNonZero(mask) > 0:
        # print("1")
        return True
    else:
        # print("2")
        return False


import numpy as np
import cv2
from PIL import ImageGrab, Image


def process_image(left, top, right, bottom):
    # 截取屏幕上指定区域的图像
    im = ImageGrab.grab(bbox=(left, top, right, bottom))
    # 获取图像的宽度和高度
    width, height = im.size
    # 创建新的空白图像
    new_im = Image.new('RGB', (width, height), color='white')
    # 遍历图像的每一个像素
    for x in range(width):
        for y in range(height):
            color = im.getpixel((x, y))
            # 判断像素的RGB值是否都低于50
            if all(c < 110 for c in color[:3]):
                # 记录黑色像素
                new_im.putpixel((x, y), (0, 0, 0))
            else:
                # 记录白色像素
                new_im.putpixel((x, y), (255, 255, 255))
    return new_im


import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def process_image2(image):
    # 将图像转为灰度图像
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 对图像进行二值化处理
    _, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # 将图像转为 PIL Image 对象
    pil_image = Image.fromarray(thresh)
    # 识别图像中的数字
    text = pytesseract.image_to_string(pil_image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    # 打印识别结果
    # print(text)
    return text


def julishibie(left, top, right, bottom):
    new_im = process_image(left, top, right, bottom)
    # new_im.show()  # 显示新的图像
    new_im_np = np.array(new_im)
    return process_image2(new_im_np)
