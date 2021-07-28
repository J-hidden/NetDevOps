自动化运维学习模板

注：这并不算得上是一个好的项目，但是肯定是一个好的初学者学习的模板，因为里面集成各种方法

一、models文件为已安装的模块的集合,虽然此项目使用的是虚拟环境，但是难免会出现环境的不对应，所以可以使用一下命令来重置项目环境
	pip3 install -r requirements.txt
	python3 manage.py collectstatic
	python3 manage.py migrate

二、项目中有使用很多方法，可以自行探索
	2.1、项目里使用了FBV和CBV
	2.2  url中使用了多种引入views的方法
	2.3  在收集交换机信息时使用了ntc_textfsm和直接调用textfsm方法

三、启动项目时建议使用以下命令启动
	python3 manage.py runserver 0:8000.  #因为在项目尾部其他链接处外链了simpleui的admin后台。如果更改端口号则此处也要更改

四、项目中收集信息的脚本都是通过schedule_coll.py来收集，请同时启动该脚本，该脚本会一直启动实时收集设备信息

