from netmiko import ConnectHandler


show_intf_cmd_mapping = {
    'cisco_ios': 'show interface',
    'huawei': 'display interface description'
}

# 需要使用textfsm更改输出的结果为列表，便于后期对输出结果解析提取关键字
def ssh_device_2_get_intf(device_type, ip, username, password, port=22):
    dev_info = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
        'port': port
    }

    cmd = show_intf_cmd_mapping.get(device_type)
    if not cmd:
        raise Exception('暂不支持此类型设备')

    with ConnectHandler(**dev_info) as net_conn:
        intfs = net_conn.send_command(cmd, use_textfsm=True)
        return intfs


if __name__ == '__main__':
    dev_info = {
        'device_type': 'huawei',
        'ip': '172.21.254.18',
        'username': 'lixilei',
        'password': 'Roward*8@li',
        'port': '22'
    }
    ssh_device_2_get_intf(**dev_info)
