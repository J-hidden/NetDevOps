from django.contrib import admin
from cmdb.models import Device, Interface, Ap, Version
from import_export.admin import ImportExportModelAdmin
# Register your models here.


@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    # 列表页显示那些字段（列）
    list_display = ['device', 'name', 'phy', 'protocol', 'desc']
    search_fields = ['name', 'desc', ]
    list_filter = ['name', 'desc', 'device', 'phy', 'protocol']


@admin.register(Ap)
class ApAdmin(admin.ModelAdmin):
    # 列表页显示那些字段（列）
    list_display = ['device', 'mac', 'name', 'group', 'ip', 'type', 'state', 'sta', 'update_time',]
    search_fields = ['mac', 'ip', 'state']
    list_filter = ['mac', 'ip', 'state']


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    # 列表页显示那些字段（列）
    list_display = ['device', 'product_version', 'uptime', 'vrp_version']
    search_fields = ['product_version', 'uptime', 'vrp_version']
    list_filter = ['product_version', 'uptime', 'vrp_version']


@admin.register(Device)
class DeviceAdmin(ImportExportModelAdmin):
    # 列表页显示那些字段（列）
    list_display = ['id', 'ip', 'username', 'password', 'name', 'platform', 'vendor', 'is_virtual', 'role']

    # 点击此字段可进行跳转详情页
    list_display_links = ['id', 'ip', 'name', 'vendor']

    # 搜索字段
    search_fields = ['id', 'ip', 'name', 'vendor']

    # 每页显示多少条记录
    list_per_page = 20

    # #不显示字段
    # exclude = ['is_virtual']

    # 侧边过滤器
    list_filter = ['vendor', 'group']
#
#     #日期的筛选过滤，本models无，供参考
#     date_hierarchy = 'creat_time'
#     #列表页排序依据，负号代表逆序
#     ordering = ('ip', '-name')

    admin.site.site_header = '自动化管理后台'  # 设置header
    admin.site.site_title = '自动化管理后台'  # 设置title
    admin.site.index_title = '自动化管理后台'