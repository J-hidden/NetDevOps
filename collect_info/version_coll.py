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

from cmdb.models import Version, Device
from info_getters import ssh_device_2_get_version
import schedule


def collect_versions():
    devs = Device.objects.all()
    # print(devs)
    for dev in devs:
        dev_info = {
            'device_type': dev.platform,
            'ip': dev.ip,
            'username': dev.username,
            'password': dev.password,
            'port': 22
        }

        versions = ssh_device_2_get_version(**dev_info)
        for version in versions:
            print(version)
            try:
                obj, created = Version.objects.update_or_create(device=dev,
                                           defaults=dict(product_version=version['product_version'], uptime=version['uptime'], vrp_version=version['vrp_version'], device=dev))
                print(obj, created)
                print('设备:{}保存成功'.format(dev))
            except Exception as e:
                print('端口:{}保存失败，错误如下{}'.format(version, str(e)))


if __name__ == '__main__':
    collect_versions()