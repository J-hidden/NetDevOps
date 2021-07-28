import os, sys
import time

import django
from pathlib import Path

# 1、将项目的根目录填入环境变量
# 2、BASE_DIR = os.path.dirname(传入项目所在的根目录)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetDevOps.settings')
django.setup()

from cmdb.models import Interface, Device
from cmdb.info_getters import ssh_device_2_get_intf
import schedule

# 先取出交换机的所有信息，然后赋值给对应的变量，在通过ssh_device_2_get_intf函数循环获取display interface description的信息然后写入到Interface数据库中
def collect_intfs():
    devs = Device.objects.all()

    for dev in devs:
        dev_info = {
            'device_type': dev.platform,
            'ip': dev.ip,
            'username': dev.username,
            'password': dev.password,
            'port': 22
        }

        intfs = ssh_device_2_get_intf(**dev_info)
        for intf in intfs:
            try:
                # Interface(name=intf['interface'], phy=intf['phy'], protocol=intf['protocol'], desc=intf['description'], device=dev).save()
                obj, created = Interface.objects.update_or_create(name=intf['interface'], phy=intf['phy'], protocol=intf['protocol'], desc=intf['description'], device=dev,
                                           defaults=dict(name=intf['interface'], phy=intf['phy'], protocol=intf['protocol'], desc=intf['description'], device=dev)
                                           )
                print(obj, created)
                print('端口:{}保存成功'.format(intf['interface']))
            except Exception as e:
                print('端口:{}保存失败，错误如下{}'.format(intf, str(e)))

# 设置定时任务
def tasklist():
    schedule.clear()
    schedule.every(1).second.do(collect_intfs)
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    # collect_intfs()
    tasklist()