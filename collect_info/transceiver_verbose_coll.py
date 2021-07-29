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

from cmdb.models import Tansceiver, Device
from info_getters import ssh_device_2_get_transceiver_verbose, ssh_device_2_get_transceiver
import schedule


def transceiver__verbose_coll():
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
        transceivers = ssh_device_2_get_transceiver_verbose(**dev_info)
        print(transceivers)
        for transceiver in transceivers:
            try:
                obj, created = Tansceiver.objects.update_or_create(device=dev, interface=transceiver['interface'],
                                                                defaults=dict(interface=transceiver['interface'],
                                                                              rx=transceiver['rx'],
                                                                              rx_max=transceiver['rx_h'],
                                                                              rx_min=transceiver['rx_l'],
                                                                              tx=transceiver['tx'],
                                                                              tx_max=transceiver['tx_h'],
                                                                              tx_min=transceiver['tx_l'],
                                                                              device=dev))
                print(obj, created)
                print('设备:{}保存成功'.format(dev))
            except Exception as e:
                print('端口:{}保存失败，错误如下{}'.format(dev, str(e)))


def transceiver_coll():
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
        transceivers = ssh_device_2_get_transceiver(**dev_info)
        # print(transceivers)
        for trans in transceivers:
            # print(trans)
            try:
                obj, created = Tansceiver.objects.update_or_create(device=dev, interface=trans['interface'],
                                                                defaults=dict(interface=trans['interface'],
                                                                              transceiver=trans['transciver_type'],
                                                                              sn=trans['serial_no'],
                                                                              connector=trans['connector_type'],
                                                                              vendor=trans['vendor'],
                                                                              wavelength=trans['wavelength_nm'],
                                                                              device=dev))
                print(obj, created)
                print('设备:{}保存成功'.format(dev))
            except Exception as e:
                print('端口:{}保存失败，错误如下{}'.format(dev, str(e)))


if __name__ == '__main__':
    # transceiver__verbose_coll()
    transceiver_coll()