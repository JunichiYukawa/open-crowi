# OSXにポータル開発環境を作る

## gitclone

```
git clone https://github.com/bbtinc/portal.git
```

### virtualenv

```
cd portal
virtualenv venv
. venv/bin/activate
```

## odbc/freetds

```
brew install freetds --with-unixodbc
brew install unixodbc
```

### rewrite /usr/local/etc/odbc.ini
```
; /usr/local/etc/odbc.ini

[portal.dev]
Description = Portal system development database.
Driver = FreeTDS
Database = BBT
Servername = portal.dev

[portal.local]
Description = Portal system development database.
Driver = FreeTDS
Database = BBT
Servername = portal.local

```

### rewrite /usr/local/etc/odbcinst.ini
```
[ODBC]
Trace = No
ForceTrace = No

[FreeTDS]
Description = TDS driver (Sybase/MS SQL)
Driver = /usr/local/lib/libtdsodbc.so
Setup = /usr/local/lib/libtdsodbc.so
UsageCount = 1
Trace = No
```

### rewrite /usr/local/etc/freetds.conf
```
#   $Id: freetds.conf,v 1.12 2007-12-25 06:02:36 jklowden Exp $
#
# This file is installed by FreeTDS if no file by the same
# name is found in the installation directory.
#
# For information about the layout of this file and its settings,
# see the freetds.conf manpage "man freetds.conf".

# Global settings are overridden by those in a database
# server specific section
[global]
text size = 4294967295

[portal.dev]
host = 10.0.2.118
port = 1433
tds version = 8.0
client charset = UTF-8

[portal.local]
host = 127.0.0.1
port = 1401
tds version = 8.0
client charset = UTF-8
```

## memcached

```
brew install memcached
sudo brew services start memcached
```

check memcached
```
telnet localhost 11211
```

もしかしたら失敗するかも

## Django

### settingsを書き換える

下記はPortalの例です。
 - DATABASESの向き先を変更する
 - DEVELOPERの定義
 - CACHEをlocalhostを向くようにする
 - ログ出力標準出力のみ
 - ファイルアップロード先のディレクトリをカレントディレクトリからにする

```python
# -*- coding:utf-8 -*-
from dev import *
import bbt.lp.core.hosts as hosts


DEVELOPER = os.getenv('DEVELOPER')

DATABASES = {
    'default': {
        'ENGINE': 'django_pyodbc',
        'NAME': 'BBT',
        'USER': 'PortalUser',
        'PASSWORD': 'P@ssw0rd',
        'HOST': '',
        'PORT': '',
        'TEST_NAME': uniq_key + 'jenkins_BBT',
        'OPTIONS':  {
            'driver': 'FreeTDS',
            # ODBC DSN name defined in your odbc.ini
            'dsn': 'portal.local',
            'driver_supports_utf8': True,
            'host_is_server': True,
            'use_legacy_datetime': True,
        },
    },
    'enquete': {
        'ENGINE': 'django_pyodbc',
        'NAME': 'ENQUETE',
        'USER': 'PortalUser',
        'PASSWORD': 'P@ssw0rd',
        'HOST': '',
        'PORT': '',
        'TEST_NAME': uniq_key + 'jenkins_ENQUETE',
        'OPTIONS':  {
            'driver': 'FreeTDS',
            # ODBC DSN name defined in your odbc.ini
            'dsn': 'portal.local',
            'driver_supports_utf8': True,
            'host_is_server': True,
            'use_legacy_datetime': True,
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "localhost:11211",
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(name)s] %(levelname)s %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'datetime': {
            'format': '%(asctime)s[%(levelname)s] %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'web': {
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'web': {
            'handlers': ['web'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# お知らせ登録画面用CKEditor設定
CKEDITOR_UPLOAD_PATH = "./share/uploads"
CKEDITOR_UPLOAD_PREFIX = "./share/uploads"

# お知らせ登録時の添付ファイルパス設定
INFO_UPLOAD_PATH = "./share/information"

# Google 画像認証
GOOGLE_RECAPCHA_PUBLIC_KEY = '6LfuhfoSAAAAAKklN6vPfz-W1jkaOGMoxrKeH1f-'
GOOGLE_RECAPCHA_PRIVATE_KEY = '6LfuhfoSAAAAADsQZP-wgjwArbPVcYgvr110A37O'

ENV_NAME = 'develop.' + DEVELOPER

EXTRA_HOSTS = hosts.make(DEVELOPER + '-')

```

MacOSXではsudoで起動しないと Port80が開きません

例）
```bash
sudo env DEVELOPER=yukawa python src/manage.py test progress.ExerciseEnqueteListSQLTest --settings=settings.solution.local_mac
```

## (option)SQLServer

### box


Vagrantfile

config.vm.box_url は適宜変えてください。

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "bbt_sqlserver"
  config.vm.box_url = "file://./box/bbt_sqlserver.box"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  config.vm.network "forwarded_port", guest: 1433, host: 1401, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = "8096"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
  SHELL
end
```

## SQLServerの起動
```
vagrant up
```

## 下記はSQLServerの環境設定のための備忘録

### Create Database

```sql
CREATE DATABASE BBT;
CREATE DATABASE ENQUETE;
GO
```

check it.
```sql
select name from sys.databases;
GO
```

### Create Login User

```sql
CREATE LOGIN PortalUser WITH PASSWORD = 'P@ssw0rd';
GO
```

check it.

```
/opt/mssql-tools/bin/sqlcmd -S localhost -U PortalUser -P 'P@ssw0rd'
```

### Create Database User and setting GRANT

```sql
use master;
CREATE USER PortalUser FOR LOGIN PortalUser;
GO
GRANT ALL TO PortalUser;
GO

use BBT;
CREATE USER PortalUser FOR LOGIN PortalUser;
GO
GRANT ALL TO PortalUser;
GO

use ENQUETE;
CREATE USER PortalUser FOR LOGIN PortalUser;
GO
GRANT ALL TO PortalUser;
GO
```

## DBに初期データ投入時にエラーが出る場合は
### rewrite /usr/local/etc/odbcinst.ini
```
[ODBC]
Trace        = Yes
TraceFile    = /tmp/sql.log
ForceTrace   = Yes

[FreeTDS]
Description = TDS driver (Sybase/MS SQL)
Driver = /usr/local/lib/libtdsodbc.so
Setup = /usr/local/lib/libtdsodbc.so
UsageCount = 1
Trace = No
```
TraceFileは任意の場所に設定する。