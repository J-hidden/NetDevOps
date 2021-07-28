# Generated by Django 3.2.4 on 2021-07-19 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0010_neighbor_lldp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neighbor_lldp',
            name='Neighbor_dev',
            field=models.CharField(max_length=32, verbose_name='对端IP'),
        ),
        migrations.CreateModel(
            name='Tansceiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface', models.CharField(max_length=128, verbose_name='接口')),
                ('transceiver', models.CharField(max_length=128, verbose_name='光模块类型')),
                ('sn', models.CharField(max_length=128, verbose_name='光模块SN')),
                ('rx', models.CharField(max_length=128, verbose_name='收光')),
                ('rx_max', models.CharField(max_length=128, verbose_name='收光上限')),
                ('rx_min', models.CharField(max_length=128, verbose_name='收光下限')),
                ('tx', models.CharField(max_length=128, verbose_name='发光')),
                ('tx_max', models.CharField(max_length=128, verbose_name='发光上限')),
                ('tx_min', models.CharField(max_length=128, verbose_name='发光下限')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.device', verbose_name='设备IP')),
            ],
        ),
        migrations.CreateModel(
            name='Cpu_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage', models.CharField(max_length=128, verbose_name='CPU使用率')),
                ('stat_time', models.CharField(max_length=128, verbose_name='记录时间')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.device', verbose_name='设备IP')),
            ],
        ),
    ]