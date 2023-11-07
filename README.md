# Развертывание проекта локально и на сервере

1. Скопировать проект из гитхаба
`git clone https://github.com/zhohov/sakhalin_hack.git`
2. Переименовать `env` в `.env`
3. Заполнить данные в `.env`, для локального запуска `DB_HOST=localhost`, для сервера `DB_HOST=ip сервера`
4. Отредактировать `docker-compose`, вставить имя пользователя и пароль для `db`
5. В файле проекта `core/settings/common.py` вписать в `ALLOWED_HOSTS = []` айпи и домен
6.  Билд проекта `docker-compose build`
7. Запуск проекта `docker-compose up`
8. Просмотр логов
	1. Запустить `docker ps` 
	2. Посмотреть логи `docker logs <container_id>`
9. Для входа в админку нужно создать суперпользователя
	1. Запустить `docker ps` 
	2. Выполнить `docker exec <backend_container_id> bash`
	3. Выполнить `python manage.py createsuperuser`
10. Остановка проекта `docker-compose stop`
11. Запуск после остановки `docker-compose start`