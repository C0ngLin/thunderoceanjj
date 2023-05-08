import time
import pyautogui
from find import find, check
from until import get_resource_path, locate
from utils import active, click, logger_log as log


def find_box():
    box1 = locate(get_resource_path('pic/ok02.png'), 0.8)
    box2 = locate(get_resource_path('pic/ok03.png'), 0.8)
    box3 = locate(get_resource_path('pic/ok04.png'), 0.8)
    box4 = locate(get_resource_path('pic/chengyuanzuqueding.png'), 0.7)
    box5 = locate(get_resource_path('pic/XX.png'), 0.7)
    if box4 is not None:
        click(box4)
        time.sleep(0.1)
        log("已经重新加入")
    elif box1 is not None:
        click(box1)
        time.sleep(0.1)
    elif box2 is not None:
        click(box2)
        time.sleep(0.1)
    elif box3 is not None:
        click(box3)
        time.sleep(0.1)
    elif box5 is not None:
        click(box5)
        time.sleep(0.1)
    else:
        log('未检测到错误情况')


def join():  # 加入游戏，并且判断是否加入
    global flag
    flag = False
    while True:
        # active()
        join = locate(get_resource_path('pic/jiaruzhandou.png'), 0.7)
        time.sleep(0.5)
        if join is not None:
            click(join)
            log('加入')
            time.sleep(0.1)
            checkjoin = check(get_resource_path('pic/zhanjuzhong.png'), 0.7)
            checkship = check(get_resource_path('pic/noship2.png'), 0.7)
            if checkjoin is True:
                log('加入出现问题')
                click(checkjoin)
                try:
                    ok02 = find(get_resource_path('pic/ok02.png'))
                    click(ok02)
                    log("点击ok2")
                    ok03 = find(get_resource_path('pic/ok03.png'))
                    click(ok03)
                    log("点击ok3")
                    if ok03 is None and ok02 is None:
                        raise TypeError
                except:
                    log('未检测到错误情况')
                    continue
                time.sleep(0.1)
            else:
                log('已经成功点击')
        else:
            log('正在加入，请稍后')
            find_box()
            join1 = locate(get_resource_path('pic/haizhanzhanjuzhongjiaruzhandou.png'), 0.7)
            if join1 is not None:
                log('停止检测加入')
                break
        time.sleep(1)
        wait = locate(get_resource_path('pic/jiaruyouxi.png'), 0.8)
        time.sleep(0.5)
        if wait is not None:
            pyautogui.moveTo(10, 30)
            log('已经加入战局')
            return True


def joinship():  # 选择飞机
    i1 = 0
    while True:
        i1 = i1 + 1
        # active()
        ship = locate(get_resource_path('pic/jiaruyouxi.png'), 0.7)
        log(ship)
        time.sleep(1)
        if ship is not None:
            log('点击加入')
            click(ship)
            time.sleep(0.1)
            return True
        elif i1 > 30:
            hvj = locate(get_resource_path('pic/zhanjuzhong.png'), 0.8)
            noselectship = locate(get_resource_path('pic/jiaruyouxi1080p.png.png'), 0.8)
            if hvj is not None:
                log('游戏已经开始')
                return True
            elif noselectship is not None:
                flag_False = locate(get_resource_path('pic/flag_false.png'), 0.8)
                if flag_False is not None:
                    log('未知错误')
                    return None
                elif flag_False is None:
                    log('未选择飞机')
                    return False
            else:
                log('未能成功加入')
                return False
        else:
            log('没有飞机可以加入')
            time.sleep(2)


def main_join():
    global Fg
    pic_list = ['pic/kejishu.png', 'pic/zhanjuzhong.png', 'pic/time.png']
    for pic in pic_list:
        Fg = 0
        j = locate(get_resource_path(pic), 0.7)
        if j is not None and pic == 'pic/kejishu.png':
            log('在主菜单')
            Fg = 1
            break
        elif j is not None and pic == 'pic/zhanjuzhong.png':
            log('游戏已经开始')
            Fg = 2
            break
        elif j is not None and pic == 'pic/time.png':
            log('尚未选择船只')
            Fg = 3
            break
    if Fg == 1:
        join()
        time.sleep(0.5)
        j1 = joinship()
        if j1 is True:
            return True
        elif j1 is False:
            return False
    elif Fg == 2:
        return True
    elif Fg == 3:
        j1 = joinship()
        if j1 is True:
            return True
        elif j1 is False:
            return False
    elif Fg == 0:
        return False


if __name__ == '__main__':
    active()
    find_box()
