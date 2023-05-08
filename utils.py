import ctypes
import os
import time
import win32con
import win32gui
import dearpygui.dearpygui as dpg
import pytesseract
import cv2
import numpy as np
import pyautogui
from find import locate
from loguru import logger


def check_red_pixel(row, x1, x2):
    # 获取屏幕分辨率
    width, height = pyautogui.size()

    # 检查每个像素是否为红色像素
    red_pixels_count = 0
    for x in range(x1, x2 + 1):
        r, g, b = pyautogui.pixel(x, row)
        if r > 220 and g > 220 and b > 220:
            red_pixels_count += 1
            if red_pixels_count >= 5:
                return True
    return False
def check_red_pixel3(row, x1, x2):
    # 获取屏幕分辨率
    width, height = pyautogui.size()

    # 检查每个像素是否为红色像素
    red_pixels_count = 0
    for x in range(x1, x2 + 1):
        r, g, b = pyautogui.pixel(x, row)
        if r > 200 and g > 200 and b > 200:
            red_pixels_count += 1
            if red_pixels_count >= 5:
                return True
    return False

def check_red_pixel2(row, x1, x2):
    # 获取屏幕分辨率
    width, height = pyautogui.size()

    # 检查每个像素是否为红色像素
    red_pixels_count = 0
    for x in range(x1, x2 + 1):
        r, g, b = pyautogui.pixel(x, row)
        if r > 230 and g < 100 and b < 100:
            red_pixels_count += 1
            if red_pixels_count >= 5:
                return True
    return False






logger.remove(handler_id=None)
logger.add("wtauto_{time:YYYY-MM-DD}.log", format='{time:YYYY-MM-DD HH:mm} {level} {message}', rotation='3 days',
           encoding='UTF-8')


def active():  # 窗口置顶
    global hwnd
    hwnd = win32gui.FindWindow('DagorWClass', None)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
    win32gui.SetForegroundWindow(hwnd)


def findweizhi(a, b):
    import pyautogui
    # 指定屏幕上的位置
    x, y = a, b
    # 获取指定位置的像素颜色
    color = pyautogui.screenshot().getpixel((x, y))
    # 检查RGB值是否都小于50
    if all(c < 50 for c in color):
        return True
    else:
        return False


def recognize_digits_pytesseract(img):
    result = pytesseract.image_to_string(img, lang='eng', config=tessdata_dir_config)
    return result


# 左上角(774,490)右下角(832,506)
# 识别两个区域中的数字
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata" --psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'


def capture_screen(region):
    img = pyautogui.screenshot(region=region)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray


def recognize_regions(x, y, z, w):
    # 第一个区域左上角坐标(520,155)右下角坐标(1093,465)第二个区域左上角坐标(772,509)右下角坐标(841,536)
    # 第一个区域
    region1 = (x, y, z, w)
    # region1 = (774, 490, 61, 16)
    img1 = capture_screen(region1)
    img1 = cv2.adaptiveThreshold(img1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)
    digits1 = recognize_digits_pytesseract(img1)
    return digits1


def click(p):  # 第二种
    hwnd = win32gui.FindWindow('DagorWClass', None)
    win32gui.SetForegroundWindow(hwnd)
    x = p[0]
    y = p[1]
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.01)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
    time.sleep(0.1)
    pyautogui.moveTo(x=20, y=300)


def checklog(param):
    out = param + '\n'
    with open('check.ini', 'r+') as check:
        check.seek(0, 2)
        check.write(out)


def logger_log(param):
    try:
        logger.info(param)
        checklog(param)
        # print(param)
    except:
        logger.exception("日志异常")


def get_prefix(string):
    if len(string) == 0:
        return 0  # return "0" if string is empty
    if len(string) != 0:
        return int(string)


def coun(name):  # 读取本地有没有country文件，判断选择哪个国家
    c = os.path.exists('pic/config/country.txt')
    if c is True:
        with open('pic/config/country.txt', 'w+') as country:
            country.seek(0, 0)
            co = country.readlines()
            if co == name:
                return co
            else:
                country.truncate(0)
                country.write(name)
                co = country.readlines()
                return co
    else:
        with open('pic/config/country.txt', 'w+') as country:
            country.seek(0, 0)
            country.write(name)
            co = country.readlines()
            return co


def us():
    coun('us')
    dpg.delete_item(item='modal_id')
    logger_log('选择美国')


def ger():
    coun('ger')
    dpg.delete_item(item='modal_id')
    logger_log('选择德国')


def ussr():
    coun('ussr')
    dpg.delete_item(item='modal_id')
    logger_log('选择苏联')


def uk():
    coun('uk')
    dpg.delete_item(item='modal_id')
    logger_log('选择英国')


def jp():
    coun('jp')
    dpg.delete_item(item='modal_id')
    logger_log('选择日本')


def it():
    coun('it')
    dpg.delete_item(item='modal_id')
    logger_log('选择意呆')


def selectrun():  # 判断运行哪一个版本游戏
    st = os.path.exists('pic/config/steam.d')
    gj = os.path.exists('pic/config/gaijin.d')
    if st is True:
        logger_log('运行steam版')
        return 1
    elif gj is True:
        logger_log('运行Gaijin版')
        return 2


def selet_c():  # 选择国家
    hwnd = win32gui.FindWindow('DagorWClass', None)
    if not hwnd == 0:
        se = os.path.exists('pic/config/country.txt')
        print(se)
        if se is True:
            with open('pic/config/country.txt', 'r') as country:
                co = country.readline()
                print(co)
            if co == 'us':
                c = locate('pic/country/usa.png', 0.8)
                time.sleep(0.5)
                click(c)
                time.sleep(1)
                s = locate('pic/luncher/hang.png', 0.8)
                click(s)
                logger_log('选择完毕')
            elif co == 'ger':
                c = locate('pic/country/ger.png', 0.8)
                time.sleep(0.5)
                click(c)
                time.sleep(1)
                s = locate('pic/luncher/hang.png', 0.8)
                click(s)
                logger_log('选择完毕')
            elif co == 'ussr':
                c = locate('pic/country/ussr.png', 0.8)
                time.sleep(0.5)
                click(c)
                time.sleep(1)
                s = locate('pic/luncher/hang.png', 0.8)
                click(s)
                logger_log('选择完毕')
            elif co == 'uk':
                c = locate('pic/country/uk.png', 0.8)
                time.sleep(0.5)
                click(c)
                time.sleep(1)
                s = locate('pic/luncher/hang.png', 0.8)
                click(s)
                logger_log('选择完毕')
            elif co == 'jp':
                c = locate('pic/country/jp.png', 0.8)
                time.sleep(0.5)
                click(c)
                time.sleep(1)
                s = locate('pic/luncher/hang.png', 0.8)
                click(s)
                logger_log('选择完毕')
            elif co == 'it':
                c = locate('pic/country/it.png', 0.8)
                time.sleep(0.5)
                click(c)
                time.sleep(1)
                s = locate('pic/luncher/hang.png', 0.8)
                click(s)
                logger_log('选择完毕')
            else:
                a = False
                return a
        else:
            a = False
            return a
