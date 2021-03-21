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
* sed "s/SITENAME/vcs.anra.ml/g"  source/vcs_site/deploy_tools/nginx.template.conf  | sudo tee /etc/nginx/sites-available/vcs.anra.ml
* sudo ln -s ../sites-available/vcs.anra.ml /etc/nginx/sites-enabled/vcs.anra.ml
## Служба Systemd
* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на staging.my-domain.com
* заменить SEKRIT почтовым паролем
* sed "s/SITENAME/vcs.anra.ml/g"  source/vcs_site/deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-vcs.anra.ml.service 

## Запуск служб
* sudo systemctl daemon-reload
* sudo systemctl reload nginx
* sudo systemctl enable gunicorn-vcs.anra.ml
* sudo systemctl start gunicorn-vcs.anra.ml

## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username
/home/username 
└── sites
	└── SITENAME
		├── database
		├── source
		├── static
		└── virtualenv
