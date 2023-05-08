import time
import win32api
import win32con
import key
import presskey
from presskey import hold
from until import findheise, findhongse, findheise2
from until import locate, get_resource_path, detect_green_circle
from utils import logger_log as log, active, click


def dead():
    queding = locate(get_resource_path('pic/missioncomplete.png'), 0.7)
    fanhuijidi1080p = locate(get_resource_path('pic/fanhuijidi1080p.png'), 0.7)
    qianwangjidi1080p = locate(get_resource_path('pic/qianwangjidi1080p.png'), 0.7)
    ship = locate(get_resource_path('pic/jiaruyouxi.png'), 0.7)
    xx = locate(get_resource_path('pic/XX.png'), 0.7)
    if ship is not None:
        click(ship)
    if fanhuijidi1080p is not None:
        log("发现返回基地")
        return True
    elif qianwangjidi1080p is not None:
        log("发现前往基地")
        return True
    elif xx is not None:
        log("发现X")
        return True
    elif queding is not None:
        log("发现确定")
        return True


def danger():
    if findhongse(846, 637, 977, 655):
        log("危险情况倒车")
        hold(key.key_S, 2)
        time.sleep(60)
        hold(key.key_W, 2)
        hold(key.key_A, 20)


def start():
    for item in range(16):
        log("开始检测是否进入到游戏中")
        chuanmao = locate(get_resource_path('pic/zhanjuzhong.png'), 0.7)
        if chuanmao is not None:
            log("检测到船锚")
            break
        time.sleep(1)
    log("游戏开始")


def fly():
    start()
    # 目标检测次数
    detection = 0
    while True:
        danger()
        if detection > 8:
            hold(key.key_W, 2)
            detection = 0
        detection = detection + 1
        # 加入战斗
        if dead():
            return True
        presskey.press(key.key_X)
        presskey.press(key.key_LeftShift)
        time.sleep(0.5)
        presskey.press(key.key_P)
        time.sleep(0.5)
        if not findheise2(571, 565, 582, 566):
            presskey.press(key.key_LeftShift)
        center = detect_green_circle()
        if findheise(1352, 624, 1367, 625) or center is not None:
            presskey.press(key.key_B)
            while True:
                danger()
                if not findheise2(571, 565, 582, 566):
                    presskey.press(key.key_LeftShift)
                if dead():
                    return True
                center = detect_green_circle()
                if center is not None:
                    x = center[0] + 508
                    y = center[1] + 347
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x - 961, 0)
                    time.sleep(0.5)
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, y - 565)
                #     642,385
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                time.sleep(0.1)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                if not findheise(1352, 624, 1367, 625) and center is None:
                    log("目标消失")
                    presskey.press(key.key_P)
                    center = detect_green_circle()
                    if not findheise(1352, 624, 1367, 625) and center is None:
                        log("目标确认消失")
                        break
        else:
            log("寻找目标中")
            presskey.press(key.key_LeftShift)
            time.sleep(1)
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 900, 0)


if __name__ == '__main__':
    active()
    ship = locate(get_resource_path('pic/XX.png'), 0.6)
    print(ship)
    # fly()
