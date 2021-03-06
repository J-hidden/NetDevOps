# Generated by Django 3.2.4 on 2021-07-08 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0005_device_port'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(max_length=128, verbose_name='目标')),
                ('action', models.CharField(max_length=128, verbose_name='行为')),
                ('status', models.CharField(max_length=128, verbose_name='状态')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='操作时间')),
                ('message', models.CharField(max_length=128, verbose_name='信息')),
            ],
        ),
        migrations.CreateModel(
            name='Ap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac', models.CharField(max_length=128, verbose_name='MAC')),
                ('name', models.CharField(max_length=128, verbose_name='名称')),
                ('group', models.CharField(max_length=128, verbose_name='分组')),
                ('ip', models.GenericIPAddressField(verbose_name='IP地址')),
                ('type', models.CharField(max_length=128, verbose_name='AP设备类型')),
                ('state', models.CharField(max_length=128, verbose_name='状态')),
                ('sta', models.CharField(max_length=128, verbose_name='在线客户端')),
                ('update_time', models.CharField(max_length=128, verbose_name='更新时间')),
                ('device', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='cmdb.device', verbose_name='IP地址')),
            ],
            options={
                'unique_together': {('mac', 'device', 'ip')},
            },
        ),
    ]
