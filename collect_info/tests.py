from django.test import TestCase
from netmiko import ConnectHandler
# Create your tests here.


dev_info = {
    'device_type': 'huawei',
    'ip': '172.21.254.18',
    'username': 'lixilei',
    'password': 'Roward*8@li',
    'port': '22'
}

show_intf_cmd_mapping = {
    'cisco_ios': 'show interface',
    'huawei': 'display interface description'
}

cmd = show_intf_cmd_mapping.get('huawei')

with ConnectHandler(**dev_info) as conn:
    output = conn.send_command(cmd, use_textfsm=True)
    print(output)