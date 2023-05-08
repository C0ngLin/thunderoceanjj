import time
from find import locate, find_match, check
from until import get_resource_path
from utils import logger_log as log, click, active


def cantjoin():  # 加入失败
    while True:
        active()
        error1 = find_match(get_resource_path('pic/jiaruzhandou.png'), 0.7)
        if error1 is not None:
            log('检测到加入战斗按钮')
            p = 10, 30
            click(p)
            chkerr1 = check(get_resource_path('pic/jiaruzhandou.png'), 0.7)
            if chkerr1 is True:
                break
        else:
            break


def main_end():
    global flag_back
    flag_back = False
    while True:
        # active()
        if flag_back is False:
            log('正在检测是否有其他要素')
            pic_list = {'pic/lingqu.png', 'pic/res01.png', 'pic/ok02.png', 'pic/queding.png',
                        'pic/ok04.png', 'pic/rescom.png', 'pic/close.png', 'pic/completeres.png',
                        'pic/goumai.png', 'pic/checkin.png', 'pic/qianwangjidi1080p.png',
                        'pic/shequ.png', 'pic/fou.png', 'pic/yanfa.png', 'pic/cha.png', 'pic/fanhuijidi1080p.png',
                        'pic/queding1080p.png', 'pic/missioncomplete.png', 'pic/queding2.png', 'pic/queding3.png',
                        'pic/XX.png'}
            for pic in pic_list:
                a = locate(get_resource_path(pic), 0.7)
                log(pic)
                time.sleep(0.5)
                if a is not None:
                    if pic == 'pic/lingqu.png':
                        menu = locate(get_resource_path('pic/lost.png'), 0.8)
                        if menu is not None:
                            click(a)
                            log('开箱子')
                    elif pic == 'pic/res01.png':
                        click(a)
                        log('分配研发')
                    elif pic == 'pic/XX.png':
                        click(a)
                        log('点击X')
                    elif pic == 'pic/missioncomplete.png':
                        click(a)
                        log('点击确定')
                    elif pic == 'pic/queding2.png':
                        click(a)
                        log('点击确定2')
                    elif pic == 'pic/queding3.png':
                        click(a)
                        log('点击确定3')
                    elif pic == 'pic/queding1080p.png':
                        click(a)
                        log('点击确定')
                    elif pic == 'pic/fanhuijidi1080p.png':
                        click(a)
                        log('返回基地')
                    elif pic == 'pic/fou.png':
                        click(a)
                        log("检测到否")
                    elif pic == 'pic/ok02.png':
                        click(a)
                        log('确定')
                    elif pic == 'pic/yanfa.png':
                        click(a)
                        log("点击研发")
                    elif pic == 'pic/ok04.png':
                        click(a)
                        log('确定')
                    elif pic == 'pic/rescom.png':
                        click(a)
                        log('研发载具')
                    elif pic == 'pic/close.png':
                        click(a)
                        log('关闭其他')
                    elif pic == 'pic/completeres.png':
                        click(a)
                        log('完成研发')
                    elif pic == 'pic/goumai.png':
                        log("检测到购买")
                        notbuy = locate(get_resource_path('pic/cha.png'), 0.7)
                        no = locate(get_resource_path('pic/fou.png'), 0.7)
                        if notbuy is not None:
                            time.sleep(0.5)
                            click(notbuy)
                            log('点击×')
                        elif no is not None:
                            time.sleep(0.5)
                            click(no)
                            log('点击×')
                    elif pic == 'pic/tectree.png':
                        p = (20, 60)
                        click(p)
                        log('关闭科技树')
                    elif pic == 'pic/checkin.png':
                        log("检测到领取奖励")
                        menu = locate(get_resource_path('pic/lost.png'), 0.8)
                        if menu is not None:
                            click(a)
                            log('签到')
                            time.sleep(8)
                            lingquqiandao = locate(get_resource_path('pic/close.png'), 0.8)
                            time.sleep(0.5)
                            click(lingquqiandao)
                            log('领取成功')
                    elif pic == 'pic/qianwangjidi1080p.png':
                        click(a)
                        log('返回基地')
                    elif pic == 'pic/shequ.png':
                        log("检测到社区")
                        time.sleep(2)
                        kejishu = locate(get_resource_path('pic/kejishu.png'), 0.7)
                        if kejishu is not None:
                            flag_back = True
                            log('循环结束，已经在主菜单')
                            break
                        else:
                            continue
                    elif pic == 'pic/queding.png':
                        click(a)
                        log('点击确定，可能有其他待点击资源')
                        time.sleep(5)
                        wait_for_match = ['pic/completeres.png', 'pic/rescom.png', 'pic/res01.png']
                        for wait_pic in wait_for_match:
                            wait_pic_loc = locate(get_resource_path(wait_pic), 0.7)
                            stop = locate(get_resource_path('pic/shequ.png'), 0.7)
                            time.sleep(0.5)
                            if wait_pic_loc is not None:
                                if wait_pic_loc == 'pic/completeres.png':
                                    click(wait_pic_loc)
                                    log('完成研发')
                                    time.sleep(0.5)
                                elif wait_pic_loc == 'pic/rescom.png':
                                    log(wait_pic_loc)
                                    log('研发载具')
                                    time.sleep(0.5)
                                elif wait_pic_loc == 'pic/res01.png':
                                    log(wait_pic_loc)
                                    log('分配研发')
                                    time.sleep(0.5)
                            elif stop is not None:
                                flag_back = True
                                log('循环结束')
                                break
        else:
            break
    cantjoin()
    return True


if __name__ == '__main__':
    active()
    main_end()
