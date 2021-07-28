from django.db import models

# Create your models here.


# 建立用户账密的数据库
class Users(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=128)
    password = models.CharField(verbose_name='密码', max_length=128)
    email = models.EmailField(verbose_name='邮箱')


# 建立设备信息的数据库
class Device(models.Model):
    group_choices = (
        ('0', '一组'),
        ('1', '二组'),
        ('2', '三组'),
    )
    ip = models.GenericIPAddressField(verbose_name='IP地址', unique=True)
    name = models.CharField(verbose_name='设备名称', max_length=128)
    username = models.CharField(verbose_name='用户名', default='lixilei',max_length=128)
    password = models.CharField(verbose_name='密码', default='lixilei6028', max_length=128)
    port = models.CharField(verbose_name='端口', default=22, max_length=128)
    platform = models.CharField(verbose_name='平台(netmiko)', max_length=128)
    sn = models.CharField(verbose_name='sn', max_length=128, unique=True,)
    vendor = models.CharField(verbose_name='厂商', max_length=128)
    role = models.CharField(verbose_name='设备类型', max_length=128,)
    is_virtual = models.BooleanField(verbose_name='虚拟化', default=False)
    group = models.CharField(verbose_name='运维组', choices=group_choices,  max_length=128)
    creat_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def __str__(self):
        return '{}:{}'.format(self.ip, self.name)

# 接口状态以及描述的数据库
class Interface(models.Model):
    name = models.CharField(verbose_name='端口名称', max_length=256)
    phy = models.CharField(verbose_name='物理接口状态', max_length=256)
    protocol = models.CharField(verbose_name='逻辑接口状态', max_length=256)
    desc = models.CharField(verbose_name='端口描述', max_length=256)
    device = models.ForeignKey('Device', verbose_name='IP地址', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'device')

    def __str__(self):
        return '{}'.format(self.device)


# 建立AP信息的数据库
class Ap(models.Model):
    mac = models.CharField(verbose_name='MAC', max_length=128)
    name = models.CharField(verbose_name='名称', max_length=128)
    group = models.CharField(verbose_name='分组', max_length=128)
    ip = models.GenericIPAddressField(verbose_name='IP地址', max_length=128)
    type = models.CharField(verbose_name='AP设备类型', max_length=128)
    state = models.CharField(verbose_name='状态', max_length=128)
    sta = models.CharField(verbose_name='在线客户端', max_length=128)
    update_time = models.CharField(verbose_name='更新时间', max_length=128)
    device = models.ForeignKey('Device', verbose_name='IP地址', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('mac', 'device', 'ip')

    def __str__(self):
        return '{}:{}'.format(self.ip, self.state)

# 建立版本的数据库
class Version(models.Model):
    product_version =models.CharField(verbose_name='产品版本', max_length=128)
    uptime = models.CharField(verbose_name='更新时间', max_length=128)
    vrp_version = models.CharField(verbose_name='虚拟版本', max_length=128)
    device = models.ForeignKey('Device', verbose_name='IP地址', on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{}'.format(self.device, self.vrp_version)


# 建立lldp邻居的数据库
class Neighbor_lldp(models.Model):
    Local_intf = models.CharField(verbose_name='本地接口', max_length=128)
    Neighbor_dev = models.CharField(verbose_name='对端IP', max_length=32)
    Neighbor_intf = models.CharField(verbose_name='对端接口', max_length=128)
    device = models.ForeignKey('Device', verbose_name='本地地址', on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{}'.format(self.device,self.Neighbor_dev)

# 建立Log日志的数据库
class Log(models.Model):
    target = models.CharField(verbose_name='目标', max_length=128)
    action = models.CharField(verbose_name='行为', max_length=128)
    status = models.CharField(verbose_name='状态', max_length=128)
    time = models.DateTimeField(verbose_name='操作时间', auto_now_add=True)
    message = models.CharField(verbose_name='信息', max_length=128)

    def __str__(self):
        return '{}:{}'.format(self.target, self.action)


# 创建交换机CPU使用率数据库
class Cpu_info(models.Model):
    usage = models.CharField(verbose_name='CPU使用率', max_length=128)
    stat_time = models.CharField(verbose_name='记录时间', max_length=128)
    device = models.ForeignKey(Device, verbose_name='设备IP', on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{}'.format(self.device, self.usage)


# 创建交换机光功率
class Tansceiver(models.Model):
    interface = models.CharField(verbose_name='接口', max_length=128)
    transceiver = models.CharField(verbose_name='光模块类型', max_length=128)
    sn = models.CharField(verbose_name='光模块SN', max_length=128)
    connector = models.CharField(verbose_name='连接类型', max_length=128,)
    vendor = models.CharField(verbose_name='生产厂商', max_length=128,)
    wavelength = models.CharField(verbose_name='波长', max_length=128,)
    rx = models.CharField(verbose_name='收光', max_length=128)
    rx_max = models.CharField(verbose_name='收光上限', max_length=128)
    rx_min = models.CharField(verbose_name='收光下限', max_length=128)
    tx = models.CharField(verbose_name='发光', max_length=128)
    tx_max = models.CharField(verbose_name='发光上限', max_length=128)
    tx_min = models.CharField(verbose_name='发光下限', max_length=128)
    device = models.ForeignKey(Device, verbose_name='设备IP', on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{}'.format(self.device, self.interface)
