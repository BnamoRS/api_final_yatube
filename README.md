# api_yatube

## Описание

api_yatube - приложение, реализующее API интерфейс для проекта Yatube.

API доступен только аутентифицированным пользователям. Аутентификация осуществляется по токену TokenAuthenticaton.
Аутентифицированный пользователь авторизован на изменение и удаление своего контента; в остальных случаях доступ предоставляется только для чтения.

Доступные эндпоинты в API:
* `api/v1/api-token-auth/ (POST)`: передаём логин и пароль, получаем токен.
* `api/v1/posts/ (GET, POST)`: получаем список всех постов или создаём новый пост.
* `api/v1/posts/{post_id}/ (GET, PUT, PATCH, DELETE)`: получаем, редактируем или удаляем пост по id.
* `api/v1/groups/ (GET)`: получаем список всех групп.
* `api/v1/groups/{group_id}/ (GET)`: получаем информацию о группе по id.
* `api/v1/posts/{post_id}/comments/ (GET, POST)`: получаем список всех комментариев поста с `id=post_id` или создаём новый, указав id поста, который хотим прокомментировать.
* `api/v1/posts/{post_id}/comments/{comment_id}/ (GET, PUT, PATCH, DELETE)`: получаем, редактируем или удаляем комментарий по id у поста с `id=post_id`.

В ответ на запросы POST, PUT и PATCH API возвращает объект, который был добавлен или изменён.

## Зависимости

* Python 3.7
* django 2.2.16
* djangorestframework 3.12.4
* requests 2.26.0
* Pillow 8.3.1
* sorl-thumbnail 12.7.0

## Установка

После клонирования репозитория необходимо установить виртуальное окружение:
```bash
python -m venv venv
```
Активировать виртуальное оружение:
```bash
source ./venv/Scripts/activate
```
Установить зависимости из файла `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Автор

***Роман Буцких***

## Примеры

Для тестирования можно запустить тестовый сервер Django из каталога где расположен файл `manage.py` командой:
```bash
    python manage.py runserver
```
Для запросов можно использовать служебную программу командной строки `curl`.

**Примеры запросов:**

`POST` запрос - получение токена:
```
    curl --location --request POST 'http://127.0.0.1:8000/api/v1/api-token-auth/' --header 'Authorization: Token 1e**********a2' --header 'Content-Type: application/json' --data-raw '{"username": "user", "password": "u******r"}'
```

`GET` запрос - получение списка постов:
```
    curl --location --request GET 'http://127.0.0.1:8000/api/v1/posts/' --header 'Authorization: Token 1e**********a2' --data-raw ''
```

`POST` запрос - создание нового поста:
```
    curl --location --request POST 'http://127.0.0.1:8000/api/v1/posts/' --header 'Authorization: Token 1e**********a2' --header 'Content-Type: application/json' --data-raw '{"text": "new post", "group": "1"}'
```