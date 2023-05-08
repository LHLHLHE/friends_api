# Friends API

## Запуск

Перейти в директорию с файлом __manage.py__ и выполнить команды:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
### Запуск в контейнере
```
docker build .
docker run -d --name friends_api -it -p 8000:8000 friends_api
```
Затем зайдите в терминал контейнера:
```
docker exec -ti friends_api bash
```
И выполните команды:
```
python manage.py makemigrations
python manage.py migrate
exit
```
## Использование
Сервис будет доступен по адресу http://127.0.0.1:8000
### Примеры использования
Пример регитрации и авторизации пользователя:
- Регистрация: __POST 127.0.0.1:8000/api/v1/users/__
```
{
    "username": "username1",
    "password": "adgsdrfgd1"
}
```
- Авторизация: __POST 127.0.0.1:8000/auth/token/login/__
```
{
    "username": "username1",
    "password": "adgsdrfgd1"
}
```
При авторизации в ответ придет токен, который нужно передавать в заголовке при последующих запросах.

#### OpenAPI спецификация доступна по http://127.0.0.1:8000/api/v1/redoc/.