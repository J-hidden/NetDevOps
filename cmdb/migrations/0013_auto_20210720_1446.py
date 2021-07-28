# Generated by Django 3.2.4 on 2021-07-20 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0012_auto_20210720_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tansceiver',
            name='connector',
            field=models.CharField(max_length=128, verbose_name='连接类型'),
        ),
        migrations.AlterField(
            model_name='tansceiver',
            name='vendor',
            field=models.CharField(max_length=128, verbose_name='生产厂商'),
        ),
        migrations.AlterField(
            model_name='tansceiver',
            name='wavelength',
            field=models.CharField(max_length=128, verbose_name='波长'),
        ),
    ]
