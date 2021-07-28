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

from cmdb.models import Cpu_info, Device
from info_getters import ssh_device_2_get_cpu_usage
import schedule


def collect_cpu_info():
    devs = Device.objects.all()
    for dev in devs:
        dev_info = {
            'device_type': dev.platform,
            'ip': dev.ip,
            'username': dev.username,
            'password': dev.password,
            'port': dev.port
        }
        cpu_usages  = ssh_device_2_get_cpu_usage(**dev_info)
        for cpu_usage in cpu_usages:
            try:
                obj, created = Cpu_info.objects.update_or_create(device=dev,
                                                       defaults=dict(usage=cpu_usage['usage'], stat_time=cpu_usage['stat_time'], device=dev))
                print(obj, created)
                print('设备:{}保存成功'.format(dev.ip))
            except Exception as e:
                print('设备:{}保存失败，错误如下{}'.format(dev.ip, str(e)))


if __name__ == '__main__':
    collect_cpu_info()