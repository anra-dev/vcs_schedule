from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random

REPO_URL = 'https://github.com/anra-dev/vcs_schedule.git'
DJANGO_PROJECT_NAME = 'vcs_site'
KEY_FILE_PATH = '~/PycharmProjects/vcs_schedule/vcs_site/key.py'
ROOT_NAME = 'ubuntu'


def deploy():
    """развернуть"""
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_key_file(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _load_fixture(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    """создает структуру каталогов если нужно"""
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    """получить самый свежий исходный код"""
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    """обновить настройки"""
    settings_path = source_folder + '/' + DJANGO_PROJECT_NAME + '/settings.py'
    # Выключаем режим отладки
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'ALLOWED_HOSTS =.+$', f'ALLOWED_HOSTS = ["{site_name}"]')
    # Генерируем новый ключ
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^*(-_=+)'
    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    sed(settings_path, 'SECRET_KEY = .+$', f'SECRET_KEY = "{key}"')
    # Меняем путь к базе
    sed(settings_path, 'db.sqlite3', '../database/db.sqlite3')


def _update_virtualenv(source_folder):
    """обновить виртуальную среду"""
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + 'bin/pip'):
        run(f'python3 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_key_file(source_folder):
    local(f"scp {KEY_FILE_PATH} {ROOT_NAME}@{env.host}:{source_folder}/{DJANGO_PROJECT_NAME}/", capture=True)


def _update_static_files(source_folder):
    """обновить статические файлы"""
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    """обновить базу данных"""
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')


def _load_fixture(source_folder):
    """Загрузка первоначальных данных в базу"""
    run(f'cd {source_folder} && ../virtualenv/bin/python manage.py loaddata fixtures/data.json')
