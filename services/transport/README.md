Info for Developers:

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
#=# MAC OS
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

HOMEBREW{
- Homebrew_link: https://coolestguidesontheplanet.com/installing-homebrew-on-os-x-el-capitan-10-11-package-manager-for-unix-apps/
- install Xcode from Appstore (Можно обойтись и command line tools)
- get command line tools: $ xcode-select --install
- install homebrew: $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
}

RABBITMQ{
- before install Erlang
- simple way (with Homebrew): https://www.rabbitmq.com/install-homebrew.html
- other: https://www.rabbitmq.com/install-standalone-mac.html
- ~/.bash_profile: PATH=$PATH:/usr/local/sbin
}

VAGRANT{
- install virtualbox: $ brew cask install virtualbox
- install vagrant: $ brew cask install vagrant
- install vagrant-manager: $ brew cask install vagrant-manager
- add centos/7: $ vagrant box add centos/7
}

ORACLE{
- Скачиваем:
    instantclient-basic-macos.x64-11.2.0.4.0.zip
	instantclient-jdbc-macos.x64-11.2.0.4.0.zip
	instantclient-sdk-macos.x64-11.2.0.4.0.zip
	instantclient-sqlplus-macos.x64-11.2.0.4.0.zip
	instantclient-tools-macos.x64-11.2.0.4.0.zip
- распаковываем все в одну папку (по-умолчанию unzip все сделает)
    $ unzip *.zip
- переходим в распакованную папку
- устанавливаем simlink на библы, находясь в ../instantclient_11_2:
	$ ln -s libclntsh.dylib.11.1 libclntsh.dylib
	$ ln -s libocci.dylib.11.1 libocci.dylib
- прописываем пути в bash_profile:
	export ORACLE_HOME=~/Soft/DB/ORACLE/instantclient_11_2/
	export PATH=$ORACLE_HOME:$PATH
	export DYLD_LIBRARY_PATH=$ORACLE_HOME
	export LD_LIBRARY_PATH=$ORACLE_HOME
- обновляем bash:
    $ . ~/.bash_profile
- $ pip install cx_Oracle
- если ругается на libclntsh.dylib.11.1 - проверяем .bash_profile
- $ (python) import cx_Oracle
}

TROUBLES{
- ошибки импорта top-level  packages при запуске скрипта как самостоятельной идиницей
- How to fix: запускать скрипт с top-level
- link: http://stackoverflow.com/questions/16981921/relative-imports-in-python-3
}