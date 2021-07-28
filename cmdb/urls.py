from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from cmdb.views import home, Sw_info_list, Fw_info_list, Ac_info_list, Ap_info_list, Display_interface_description, Version_info_list, Neighbor_lldp_info_list
from . import views

urlpatterns = [
    path('register/', views.Register, name='register'),
    path('login/', views.Login),
    path('index/', views.index),
    url(r'^$', home, name='home'),
    path('config/', views.Config, name='config'),
    path('config_save/', views.Config_save, name='config_save'),
    path('Log_message/', views.Log_message, name='log_message'),
    path('sw_info_list/', Sw_info_list.as_view(), name='sw_info_list'),
    path('fw_info_list/', Fw_info_list.as_view(), name='fw_info_list'),
    path('ac_info_list/', Ac_info_list.as_view(), name='ac_info_list'),
    path('ap_info_list/', Ap_info_list.as_view(), name='ap_info_list'),
    path('version_info_list/', Version_info_list.as_view(), name='version_info_list'),
    path('neighbor_lldp_info_list/', Neighbor_lldp_info_list.as_view(), name='neighbor_lldp_info_list'),
    path('display_interface_description/', Display_interface_description.as_view(), name='display_interface_description'),
    path('cpu_usage/', views.Cpu_usage.as_view(), name='cpu-usage'),
    path('transceiver_info/', views.Transceiver_info.as_view(), name='transceiver_info'),
]
