from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views import View
from .models import Device, Interface, Log, Ap, Version, Users ,Neighbor_lldp, Cpu_info, Tansceiver
from django.db.models import Q
import paramiko
import time
from datetime import datetime
from netmiko import ConnectHandler
import os
import hashlib


# Create your views here.
# ---------------------------
# 问题记录处
# 1、目前查询不能多条件查询，只能单条件查询
# ------------------------
# 加密算法
def SetPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    return str(password)


def Register(request):
    if request.method=='PSOT' and request.POST:
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        Users.objects.create(
            username=username,
            password=password,
        )
        return HttpResponseRedirect('/login/')
    return render(request, 'register.html')

def Login(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')


def home(request):
    all_device = Device.objects.all()
    cisco_device = Device.objects.filter(vendor='思科')
    huawei_device = Device.objects.filter(vendor='华为')
    last_10_event = Log.objects.all().order_by('-id')[:10]
    context = {'all_device': len(all_device),
               'cisco_device': len(cisco_device),
               'huawei_device': len(huawei_device),
               'last_10_event': last_10_event
              }
    return render(request, 'home.html', context)


# 定义一个类，用来查询交换机信息，然后可以通过POST请求来筛选对应的信息
class Sw_info_list(View):
    def get(self, request):
        sw_info_list = Device.objects.filter(role='交换机')
        return render(request, 'sw_info_list.html', {'sw_info_list': sw_info_list})

    def post(self, request):
        ip = request.POST['ip']
        vendor = request.POST['vendor']
        group = request.POST['group']
        dev = Device.objects.filter(Q(ip=ip) | Q(vendor=vendor) | Q(group=group), role='交换机')
        return render(request, 'sw_info_list.html', {'sw_info_list': dev})


class Fw_info_list(View):
    def get(self, request):
        fw_info = Device.objects.filter(role='防火墙')
        return render(request, 'fw_info_list.html', {'fw_info_list': fw_info})

    def post(self, request):
        ip = request.POST['ip']
        platform = request.POST['platform']
        group = request.POST['group']
        dev = Device.objects.filter(Q(ip=ip) | Q(platform=platform) | Q(group=group), role='防火墙')
        return render(request, 'fw_info_list.html', {'fw_info_list': dev})


class Ac_info_list(View):
    def get(self, request):
        ac_info = Device.objects.filter(role='AC')
        return render(request, 'ac_info_list.html', {'ac_info_list': ac_info})

    def post(self, request):
        ip = request.POST['ip']
        vendor = request.POST['vendor']
        group = request.POST['group']
        dev = Device.objects.filter(Q(ip=ip) | Q(vendor=vendor) | Q(group=group), role='AC')
        return render(request, 'ac_info_list.html', {'ac_info_list': dev})


class Ap_info_list(View):
    def get(self, request):
        ap_info_list = Ap.objects.all()
        return render(request, 'ap_info_list.html', {'ap_info_list': ap_info_list})

    def post(self, request):
        mac = request.POST['mac']
        device = request.POST['device']
        ip = request.POST['ip']
        type = request.POST['type']
        state = request.POST['state']
        dev = Ap.objects.filter(Q(mac=mac) | Q(device__ip=device) | Q(ip=ip) | Q(type=type) | Q(state=state))
        return render(request, 'ap_info_list.html', {'ap_info_list': dev})

class Display_interface_description(View):
    def get(self, request):
        display_interface_description = Interface.objects.all()
        return render(request, 'display_interface_description.html', {'display_interface_description': display_interface_description})

    def post(self, request):
        ip = request.POST['ip']
        interface = request.POST['interface']
        phy = request.POST['phy']
        protocol = request.POST['protocol']
        description = request.POST['description']
        dev = Interface.objects.filter(Q(device__ip=ip) | Q(name=interface) | Q(phy=phy) | Q(protocol=protocol) | Q(desc=description))
        return render(request, 'display_interface_description.html', {'display_interface_description': dev})


class Version_info_list(View):
    def get(self, request):
        version_info_list = Version.objects.all()
        return render(request, 'version_info_list.html', {'version_info_list': version_info_list})

    def post(self, request):
        ip = request.POST['ip']
        dev = Version.objects.filter(device__ip=ip)
        return render(request, 'version_info_list.html', {'version_info_list': dev})


class Neighbor_lldp_info_list(View):
    def get(self, request):
        neighbor_lldp_info = Neighbor_lldp.objects.all()
        return render(request, 'neighbor_lldp.html', {'neighbor_lldp_info': neighbor_lldp_info})

    def post(self, request):
        ip = request.POST['ip']
        dev = Version.objects.filter(device__ip=ip)
        return render(request, 'neighbor_lldp.html', {'version_info_list': dev})


def Config(request):
    if request.method == 'GET':
        devices = Device.objects.all()
        context = {'devices': devices,
                   'mode': '设备配置'
                   }
        return render(request, 'config.html', context)

    elif request.method == 'POST':
        result = []
        selected_device_id = request.POST.getlist('device')
        huawei_command = request.POST['huawei_command'].splitlines()
        cisco_command = request.POST['cisco_command'].splitlines()
        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip, username=dev.username, password=dev.password,
                                   look_for_keys=False)
                if dev.platform.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    result.append(f'{dev.ip}上的运行结果')
                    conn.send('conf t\n')
                    time.sleep(1)
                    for cmd in cisco_command:
                        conn.send(cmd + '\n')
                        time.sleep(1)
                        output = conn.recv(65535).decode('ascii')
                        result.append(output)
                elif dev.platform.lower() == 'huawei':
                    conn = ssh_client.invoke_shell()
                    result.append(f'{dev.ip}上的运行结果')
                    conn.send('sys\n')
                    time.sleep(1)
                    for cmd in huawei_command:
                        conn.send(cmd + '\n')
                        time.sleep(1)
                        output = conn.recv(65535).decode('ascii')
                        result.append(output)
                log = Log(target=dev.ip, action='Configure', status='Success', time=datetime.now(),
                          message='No Error')
                log.save()
            except Exception as e:
                log = Log(target=dev.ip, action='Configure', status='Error', time=datetime.now(), message=e)
                log.save()
        result = '\n'.join(result)
        return render(request, 'verify_config.html', {'result': result})


# def Config_save(request):
#     if request.method == 'GET':
#         devices = Device.objects.all()
#         return render(request, 'config_save.html', {'devices': devices})
#     elif request.method == 'POST':
#         result = []
#         selected_device_id = request.POST.getlist('device')
#         file_time = datetime.now()
#         ## 创建实时时间文件夹
#         def mkdir(file_name):
#             folder = os.path.exists(file_name)
#             if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
#                 os.makedirs(file_name)  # makedirs 创建文件时如果路径不存在会创建这个路径
#         for x in selected_device_id:
#             try:
#                 dev = get_object_or_404(Device, px=x.ip)
#                 dev_info = {'device_type':dev.platform,'ip': dev.ip , 'username':dev.username, 'password':dev.password, 'port':dev.port }
#                 if dev.platform.lower == 'cisco':
#                     conn = ConnectHandler(dev_info)
#                     output = conn.send_command('show run')
#                     time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#                     f = open(file_time+'/'+{dev.ip}+'_'+time, 'w+')
#                     f.write(output)
#                     result.append(f'{dev.ip}配置备份成功!')
#                 elif dev.platform.lower == 'huawei':
#                     conn = ConnectHandler(dev_info)
#                     output = conn.send_command('display cu')
#                     time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#                     f = open(file_time+'/'+{dev.ip}+'_'+time, 'w+')
#                     f.write(output)
#                     result.append(f'{dev.ip}配置备份成功!')
#                 log = Log(target=dev.ip, action='配置备份', status='成功', time=datetime.now(), message='NO Error')
#                 log.save()
#             except Exception as e :
#                 log = Log(target=dev.ip, action='配置备份', status='失败', time=datetime.now(), message='Error')
#                 log.save()
#                 result.append(f'{dev.ip}配置备份成功')
def Config_save(request):
    if request.method == 'GET':
        devices = Device.objects.all()
        context = {'devices': devices}
        return render(request, 'config_save.html', context)

    elif request.method == 'POST':
        result = []
        selected_device_id = request.POST.getlist('device')
        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip, username=dev.username, password=dev.password, look_for_keys=False)
                if dev.platform.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    conn.send('terminal length 0\n')
                    conn.send('show run\n')
                    time.sleep(2)
                    output = conn.recv(65535).decode('ascii')
                    now = datetime.now()
                    date = f'{now.month}_{now.day}_{now.year}'
                    path = os.getcwd()+'/'
                    f = open(path+dev.ip+'_'+date+'.txt', 'w+')
                    f.write(output)
                    result.append(f'{dev.ip}配置备份成功!')
                elif dev.platform.lower() == 'huawei':
                    conn = ssh_client.invoke_shell()
                    conn.send('display  cu\n')
                    time.sleep(2)
                    output = conn.recv(65535).decode('ascii')
                    now = datetime.now()
                    date = f'{now.month}_{now.day}_{now.year}'
                    path = os.getcwd()+'/'
                    f = open(path+dev.ip+'_'+date+'.txt', 'w+')
                    f.write(output)
                    result.append(f'{dev.ip}配置备份成功!')
                log = Log(target=dev.ip, action='Backup Configuration', status='Success', time=datetime.now(), message='No Error')
                log.save()

            except Exception as e:
                log = Log(target=dev.ip, action='Backup Configuration', status='Error', time=datetime.now(), message=e)
                log.save()
                result.append(f'{dev.ip}配置备份失败，请查看日志!')

        result = '\n'.join(result)
        return render(request, 'verify_config.html', {'result': result})

def Log_message(request):
    log_message = Log.objects.all()
    return render(request, 'log_message.html', {'log_message': log_message})


class Cpu_usage(View):
    def get(self,request):
        cpu_infos = Cpu_info.objects.all()
        return render(request, 'cpu_info.html', {'cpu_info_list': cpu_infos})

    def POST(self,request):
        ip = 'ip'
        dev = Cpu_info.objects.filter(device__ip=ip)
        return render(request, 'cpu_info.html', {'cpu_info_list': dev})


class Transceiver_info(View):
    def get(self,request):
        transceiver_infos = Tansceiver.objects.all()
        return render(request, 'transceiver_info_list.html', {'transceiver_info': transceiver_infos})

    def POST(self,request):
        ip = 'ip'
        interface = 'interface'
        dev = Cpu_info.objects.filter(Q(interface=interface) | Q(device__ip=ip))
        return render(request, 'transceiver_info_list.html', {'transceiver_info': dev})
