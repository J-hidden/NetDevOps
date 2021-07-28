import os,sys
import time

import django
from pathlib import Path

# 1、将项目的根目录填入环境变量
# 2、BASE_DIR = os.path.dirname(传入项目所在的根目录)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetDev.settings')
django.setup()

from cmdb.models import Neighbor_lldp, Device
from info_getters import ssh_device_2_get_neighbor_lldp
import schedule


def neighbor_lldp_coll():
    devs = Device.objects.all()
    for dev in devs:
        dev_info = {
            'device_type': dev.platform,
                'ip': dev.ip,
                'username': dev.username,
                'password': dev.password,
                'port': dev.port,
        }
        # print(dev.ip)
        lldp_infos = ssh_device_2_get_neighbor_lldp(**dev_info)
        print(lldp_infos)
        for lldp_info in lldp_infos:
            try:
                obj, created = Neighbor_lldp.objects.update_or_create(device=dev, Local_intf=lldp_info['local_intf'],
                                                                defaults=dict(Local_intf=lldp_info['local_intf'],Neighbor_dev=lldp_info['neighbor_dev'],Neighbor_intf=lldp_info['neighbor_intf'], device=dev))
                print(obj, created)
                print('设备:{}保存成功'.format(dev))
            except Exception as e:
                print('端口:{}保存失败，错误如下{}'.format(dev, str(e)))


if __name__ == '__main__':
    neighbor_lldp_coll()