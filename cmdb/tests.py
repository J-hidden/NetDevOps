import sys
import os
import django
from pathlib import Path
from netmiko import ConnectHandler
from django.shortcuts import HttpResponse

# 1、将项目的根目录填入环境变量
# 2、BASE_DIR = os.path.dirname(传入项目所在的根目录)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)

# 2、引入项目的环境配置，然后无需启动django项目就可以使用其配置环境了
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetDev.settings')
django.setup()

if __name__ == '__main__':
    from cmdb.models import Device
    from cmdb import models
    # 增加
    # dev = Device(
    #     ip='192.168.1.6',
    #     name='dev02',
    #     platform='huawei',
    #     vendor='huawei',
    #     is_virtual='False',
    #     group='0'
    # )
    # dev.save()
    # print(dev, dev.ip, dev.vendor)

    # 查询1
    # devs = Device.objects.all()
    # for dev in devs:
    #     print(dev)

    # 查询2
    # devs = Device.objects.get(id=1)
    # print(devs)

    # 查询3--通过filter函数进行筛选查询，可以将ip更换为username、password等其他关键词
    # devs = Device.objects.filter(ip='192.168.1.6')
    # print(devs)

    # 删除
    # dev = Device.objects.get(id=2).delete()

    # 更新
    # dev = Device.objects.update(id=1, ip='192.168.1.7')
    # print(Device.objects.all())


def ssh_device_2_get_cpu_usage():
    dev_info = {
        'device_type': 'huawei',
        'ip': '172.21.254.18',
        'username': 'lixilei',
        'password': 'Roward*8@li',
        'port': '22'
    }
    with ConnectHandler(**dev_info) as conn:
        cpu_usage = conn.send_command('display transceiver verbose', use_textfsm=True)
        print(cpu_usage)
        return cpu_usage


if __name__ == '__main__':
    ssh_device_2_get_cpu_usage()