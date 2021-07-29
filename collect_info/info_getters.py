from netmiko import ConnectHandler
from textfsm import TextFSM

intf_cmd_mapping = {
    'cisco_ios': 'show interface',
    'huawei': 'display interface description'
}
ap_cmd_mapping = {
    'cisco_ios': 'show ap all',
    'huawei': 'display ap all',
}

version_cmd_mapping ={
    'cisco_ios': 'show version',
    'huawei': 'display version',
}

neighbor_lldp_info_mapping ={
    'huawei': 'display lldp neighbor brief'
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

    cmd = intf_cmd_mapping.get(device_type)
    if not cmd:
        raise Exception('暂不支持此类型设备')

    with ConnectHandler(**dev_info) as net_conn:
        intfs = net_conn.send_command(cmd, use_textfsm=True)
        # print(intfs)
        return intfs


def ssh_device_2_get_ap(device_type, ip, username, password, port=22):
    dev_info = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
        'port': port
    }

    cmd = ap_cmd_mapping.get(device_type)
    if not cmd:
        raise Exception('暂不支持此类型设备')

    with ConnectHandler(**dev_info) as net_conn:
        aps = net_conn.send_command(cmd, use_textfsm=True)
        # print(aps)
        return aps


def ssh_device_2_get_version(device_type, ip, username, password, port=22):
    dev_info = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
        'port': port
    }

    cmd = version_cmd_mapping.get(device_type)
    if not cmd:
        raise Exception('暂不支持此类型设备')

    with ConnectHandler(**dev_info) as net_conn:
        versions = net_conn.send_command(cmd, use_textfsm=True)
        # print(versions)
        return versions


def ssh_device_2_get_neighbor_lldp(device_type, ip, username, password, port):
    dev_info = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
        'port': port
    }

    cmd = neighbor_lldp_info_mapping.get(device_type)
    if not cmd:
        raise Exception('暂不支持此设备')

    with ConnectHandler(**dev_info) as conn:
        neighbor_lldp = conn.send_command(cmd, use_textfsm=True)
        # print(neighbor_lldp)
        return neighbor_lldp


cpu_usage_mapping = {
    'huawei': 'display cpu-usage'
}


def ssh_device_2_get_cpu_usage(device_type, ip, username, password, port):
    dev_info = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
        'port': port
    }
    cmd = cpu_usage_mapping.get(device_type)
    if not cmd:
        raise Exception('暂不支持此设备')

    with ConnectHandler(**dev_info) as conn:
        cpu_usage = conn.send_command(cmd, use_textfsm=True)
        # print(cpu_usage)
        return cpu_usage


transceiver_verbose_mapping = {
    'huawei': 'display transceiver verbose'
}


def ssh_device_2_get_transceiver_verbose(device_type, ip, username, password, port):
    dev_info = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
        'port': port
    }
    cmd = transceiver_verbose_mapping.get(device_type)
    if not cmd:
        raise Exception('暂不支持此设备')

    with ConnectHandler(**dev_info) as conn:
        transceiver = conn.send_command(cmd, use_textfsm=True)
        # f = open('./templates/huawei_display_transceiver_verbose.textfsm')
        # # 调用函数TextFSM赋值变量
        # template = TextFSM(f)
        # # 调用template下的函数ParseText解析output内容
        # # print(template.ParseTextToDicts(transceiver))
        # return template.ParseTextToDicts(transceiver)
        print(transceiver)
        return transceiver

transceiver_mapping = {
    'huawei': 'display transceiver'
}


def ssh_device_2_get_transceiver(device_type, ip, username, password, port):
    dev_info = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
        'port': port
    }
    cmd = transceiver_mapping.get(device_type)
    if not cmd:
        raise Exception('暂不支持此设备')

    with ConnectHandler(**dev_info) as conn:
        transceiver = conn.send_command(cmd, use_textfsm=True)
        # f = open('templates/huawei_display_transceiver.textfsm')
        # # 调用函数TextFSM赋值变量
        # template = TextFSM(f)
        # # 调用template下的函数ParseText解析output内容
        # # print(template.ParseTextToDicts(transceiver))
        # return template.ParseTextToDicts(transceiver)
        print(transceiver)
        return transceiver


if __name__ == '__main__':
    dev_info = {
        'device_type': 'huawei',
        'ip': '172.21.254.18',
        'username': 'lixilei',
        'password': 'Roward*8@li',
        'port': '22'
    }
    # ssh_device_2_get_ap(**dev_info)
    # ssh_device_2_get_intf(**dev_info)
    # ssh_device_2_get_version(**dev_info)
    # ssh_device_2_get_neighbor_lldp(**dev_info)
    # ssh_device_2_get_cpu_usage(**dev_info)
    #
    ssh_device_2_get_transceiver_verbose(**dev_info)
    ssh_device_2_get_transceiver(**dev_info)
