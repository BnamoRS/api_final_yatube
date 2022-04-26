# api_final_yatube

## Описание

api_final_yatube - приложение, реализующее API интерфейс для проекта Yatube.

Аутентификация осуществляется по токену JWT-токен.
У неаутентифицированных пользователей доступ к API только на чтение. Аутентифицированным пользователям разрешено изменение и удаление своего контента; в остальных случаях доступ предоставляется только для чтения.

Эндпоинт `/follow/` доступен только аутентифицированным пользователям.

## Доступные эндпоинты в API:

* `api/v1/posts/ (GET, POST)`: получаем список всех постов или создаём новый пост. При `GET` запросе можно задать количество публикаций на страницу (параметр `limit`) и номер страницы с которой начать выдачу (параметр `offset`).
* `api/v1/posts/{id}/ (GET, PUT, PATCH, DELETE)`: получаем, редактируем или удаляем пост по id.
* `api/v1/groups/ (GET)`: получаем список всех групп.
* `api/v1/groups/{id}/ (GET)`: получаем информацию о группе по id.
* `api/v1/posts/{post_id}/comments/ (GET, POST)`: получаем список всех комментариев поста с `id=post_id` или создаём новый, указав `id` поста, который хотим прокомментировать.
* `api/v1/posts/{post_id}/comments/{id}/ (GET, PUT, PATCH, DELETE)`: получаем, редактируем или удаляем комментарий по id у поста с `id=post_id`. Доступно только автору комментария.
* `api/v1/follow/ (GET, POST)`: по `GET` запросу доступны все подписки пользователя, сделавшего запрос, возможен поиск по подпискам по параметру search. По `POST` запросу создается подписка на автора, указанного в переданных данных.
* `api/v1/jwt/create/ (POST)`: получение JWT-токена.
* `api/v1/jwt/refresh/ (POST)`: обновление JWT-токена.
* `api/v1/jwt/verify/ (POST)`: проверка JWT-токена.

В ответ на запросы POST, PUT и PATCH API возвращает объект, который был добавлен или изменён.

## Зависимости

* Django==2.2.16
* pytest==6.2.4
* pytest-pythonpath==0.7.3
* pytest-django==4.4.0
* djangorestframework==3.12.4
* djangorestframework-simplejwt==4.7.2
* Pillow==8.3.1
* PyJWT==2.1.0
* requests==2.26.0

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
    curl --location --request POST 'http://127.0.0.1:8000/api/v1/jwt/create/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMzI2MzI2LCJqdGkiOiJmMzYwODNhMTE0NzA0NDM2YTBiZWE2NTgyZTkxNzI1YiIsInVzZXJfaWQiOjF9.T2IecG2O2XBQmCPUMeZ2UsVJ8IYuoZmC1vbM4qBrHVk' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "resu",
    "password": "resuresu"
}'
```
### ответ:
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MTA4MTEyNiwianRpIjoiNzRiN2FiMDI1NjcwNGNhN2IwOTI3M2YyNzNkYWJiZTgiLCJ1c2VyX2lkIjo0fQ.S6eLuuoRWhozcJr182MmGm6WtnLDY4MzEG_FmpXY7pY",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxNTk5NTI2LCJqdGkiOiIwMzdiMzFmYTRmNjU0Nzg2OGNiZWJiMTFmMzRjODNjNiIsInVzZXJfaWQiOjR9.hLkTOkV0ToO4DmGSpycubLAyXhNCaSOAlHq7sw_eDdI"
}
```

`GET` запрос - получение списка постов:
```
    curl --location --request GET 'http://127.0.0.1:8000/api/v1/posts/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMzI2MzI2LCJqdGkiOiJmMzYwODNhMTE0NzA0NDM2YTBiZWE2NTgyZTkxNzI1YiIsInVzZXJfaWQiOjF9.T2IecG2O2XBQmCPUMeZ2UsVJ8IYuoZmC1vbM4qBrHVk' \
--data-raw ''
```
### ответ:
```
[
    {
        "id": 1,
        "author": "admin",
        "text": "test post 1",
        "pub_date": "2022-04-22T20:17:11.160302Z",
        "image": null,
        "group": null
    },
    {
        "id": 2,
        "author": "admin",
        "text": "test post 2",
        "pub_date": "2022-04-22T20:19:17.027937Z",
        "image": null,
        "group": null
    },
]
```

`POST` запрос - создание нового поста:
```
    curl --location --request POST 'http://127.0.0.1:8000/api/v1/posts/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMzI2MzI2LCJqdGkiOiJmMzYwODNhMTE0NzA0NDM2YTBiZWE2NTgyZTkxNzI1YiIsInVzZXJfaWQiOjF9.T2IecG2O2XBQmCPUMeZ2UsVJ8IYuoZmC1vbM4qBrHVk' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "test post"
}'
```
### ответ:
```
{
    "id": 6,
    "author": "admin",
    "text": "test post",
    "pub_date": "2022-04-26T17:31:13.027887Z",
    "image": null,
    "group": null
}
```

`POST` запрос -  повторное создание подписки
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/follow/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMzI2MzI2LCJqdGkiOiJmMzYwODNhMTE0NzA0NDM2YTBiZWE2NTgyZTkxNzI1YiIsInVzZXJfaWQiOjF9.T2IecG2O2XBQmCPUMeZ2UsVJ8IYuoZmC1vbM4qBrHVk' \
--header 'Content-Type: application/json' \
--data-raw '
{
   "following": "resu"
}
```
### ответ:
```
{
    "non_field_errors": [
        "Такая подписка уже есть"
    ]
}
```

`POST` запрос -  создание комментария к посту
```
curl --location --request POST 'http://127.0.0.1:8000/api/v1/posts/6/comments/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUxMzI2MzI2LCJqdGkiOiJmMzYwODNhMTE0NzA0NDM2YTBiZWE2NTgyZTkxNzI1YiIsInVzZXJfaWQiOjF9.T2IecG2O2XBQmCPUMeZ2UsVJ8IYuoZmC1vbM4qBrHVk' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "test comment",
    "post": "6"
}'
```
### ответ:
```
{
    "id": 2,
    "author": "admin",
    "text": "test comment",
    "created": "2022-04-26T17:35:48.425664Z",
    "post": 6
}
```