# **dns_Bind管理平台**
---
[toc]
## dns_Bind管理平台
目前主要应用于Dns记录管理
## 开发语言及框架
- 编程语言：Python2.7 + HTML + JSCripts
- 前端框架：Bootstrap
- 后端框架：Django
## 运维平台环境
- 编程语言：Python2.7
- 操作系统：Centos7
- Bind版本：1.9+
- MySql版本：5.7
## 运维平台安装部署
1. 安装python环境，这里用到pyenv多版本管理
2. 首先安装依赖

```
yum install -y readline readline-devel readline-static openssl openssl-devel openssl-static sqlite-devel bzip2-devel bzip2-libs
myssql-devel gcc python-devel

```
3.克隆pyenv

```
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
```
4.设置相关环境变量，使pyenv生效

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
exec $SHELL -l
```
5.安装项目所需要的python版本
pyenv install [版本号]
使用pyenv global [版本号]切换版本
6.安装python虚拟环境

```
pip install virtualenv virtualenvwrapper

```
7创建存放虚拟环境的目录

```
mkdir /tmp/virtualenvs #这里的目录位置可以随意
```
8.安装virtualenvwrapper

```
find / -name virtualenvwrapper.sh
vi /etc/profile #把下面两行写到文件的最下面

export VIRTUALENVWRAPPER_PYTHON=/root/.pyenv/shims/python
export WORKON_HOME=/opt/virtualenvs
source /root/.pyenv/versions/2.7.5/bin/virtualenvwrapper.sh

```
9.
```
mkvirtualenv binder #创建一个名为binder的虚拟环境
workon binder #切换到workon虚拟环境中
```

10.在/home下进入到项目binder目录中安装依赖包

```
pip install -r requirements.txt
```
11.在项目的setting文件中指定mysql

```
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'binder',  #你的库名
            'USER': 'root',    #用户
            'PASSWORD': '123456',#密码
            'HOST': '192.168.62.129',#IP
            'PORT': 3306,
            'OPTIONS':{'init_command': 'SET default_storage_engine=INNODB;'}
        }
    }

```




