Обеспечение работы нового сайта 
================================ 
## Необходимые пакеты:
* nginx
* Python 3.6 #Ставил последнюю версию
* virtualenv + pip * Git
например, в Ubuntu:
sudo add-apt-repository ppa:fkrull/deadsnakes # не использовал

sudo apt-get install nginx git python3 python3-venv
## Конфигурация виртуального узла Nginx
* см. nginx.template.conf
* заменить SITENAME, например, на staging.my-domain.com
## Служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на staging.my-domain.com
* заменить SEKRIT почтовым паролем
## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username
/home/username 
└── sites
	└── SITENAME
		├── database
		├── source
		├── static
		└── virtualenv
