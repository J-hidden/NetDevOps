import os, sys
import time

import django
from pathlib import Path

# 1、将项目的根目录填入环境变量
# 2、BASE_DIR = os.path.dirname(传入项目所在的根目录)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetDev.settings')
django.setup()

from cmdb.models import Ap, Device
from info_getters import ssh_device_2_get_ap
import schedule

# 先取出交换机的所有信息，然后赋值给对应的变量，在通过ssh_device_2_get_intf函数循环获取display interface description的信息然后写入到Interface数据库中
def collect_aps():
    devs = Device.objects.filter(role='AC')

    for dev in devs:
        dev_info = {
            'device_type': dev.platform,
            'ip': dev.ip,
            'username': dev.username,
            'password': dev.password,
            'port': 22
        }

        aps = ssh_device_2_get_ap(**dev_info)
        for ap in aps:
            try:
                # Interface(name=intf['interface'], phy=intf['phy'], protocol=intf['protocol'], desc=intf['description'], device=dev).save()
                obj, created = Ap.objects.update_or_create(mac=ap['mac'],device=dev,
                                           defaults=dict(mac=ap['mac'], name=ap['name'], group=ap['group'], ip=ap['ip'], type=ap['type'], state=ap['state'], sta=ap['sta'], update_time=ap['uptime'], device=dev)
                                           )
                print(obj, created)
                print('端口:{}保存成功'.format(ap['interface']))
            except Exception as e:
                print('端口:{}保存失败，错误如下{}'.format(ap, str(e)))


if __name__ == '__main__':
    collect_intfs()