# REST API readme

Тестовое задание компании Hammer-Systmes.
Реализовать логику и API для следующего функционала :
- Авторизация по номеру телефона. Первый запрос на ввод номера телефона. Имитировать отправку 4хзначного кода авторизации(задержку на сервере 1-2 сек). Второй запрос на ввод кода 
- Если пользователь ранее не авторизовывался, то записать его в бд 
- Запрос на профиль пользователя
- Пользователю нужно при первой авторизации нужно присвоить рандомно сгенерированный 6-значный инвайт-код(цифры и символы)
- В профиле у пользователя должна быть возможность ввести чужой инвайт-код(при вводе проверять на существование). В своем профиле можно активировать только 1 инвайт код, если пользователь уже когда-то активировал инвайт код, то нужно выводить его в соответсвующем поле в запросе на профиль пользователя
- В API профиля должен выводиться список пользователей(номеров телефона), которые ввели инвайт код текущего пользователя.
- Реализовать и описать в readme Api для всего функционала
- Создать и прислать Postman коллекцию со всеми запросами
- Залить в сеть, чтобы удобнее было тестировать(например бесплатно на https://www.pythonanywhere.com или heroku)

Мои комментарии:
- Использовал драйвер mysql поскольку на ythonanywhere нет возможности использовать PostgreSQL на бесплатном аккаунте
- В postman вручную отправлял полученный при регистрации csrftoken в headers запроса с помощью ключа X-CSRFTOKEN
- В качестве задержки сервера использовал time.sleep(2), изначально вызвал ее в таске celery, но на бесплатный хостинг не получилось все выгрузить
## Install

    git clone https://github.com/enamsaraev/hammer-systems-test.git

## Run the app

    ./manage.py runserver

## Run the tests

    pytest -rP

## Login

### Request

`POST /user/login/`

    http://127.0.0.1:8000/user/login/ | enamsaraev.pythonanywhere.com/user/login/

### Response

    HTTP/1.1 200 OK | HTTP/1.1 201 Created
    
    {
        "code": "7209"
    }

## Confirm phone number

### Request

`POST /user/confirm/`

    http://127.0.0.1:8000/user/confirm/ | enamsaraev.pythonanywhere.com/user/confirm/

### Response

    HTTP/1.1 200 OK
    
    {
        "login": True
    }

## Get user profile

### Request

`GET /user/user-profile/`

    http://127.0.0.1:8000/user/user-profile/ | enamsaraev.pythonanywhere.com/user/user-profile/

### Response

    HTTP/1.1 200 OK
    
    {
        "username": "",
        "email": "",
        "activate_code": false,
        "activeusers": []
    }

## Get user profile

### Request

`POST /user/user-profile/`

    http://127.0.0.1:8000/user/user-profile/ | enamsaraev.pythonanywhere.com/user/user-profile/

### Response

    HTTP/1.1 200 OK | HTTP/1.1 400 | HTTP/1.1 404

## Activate invite code

### Request

`POST /user-profile/activate-code/`

    http://127.0.0.1:8000/user-profile/activate-code/ | enamsaraev.pythonanywhere.com/user-profile/activate-code/

### Response

    HTTP/1.1 200 OK

    {
        "activated_profile": {
            "id": "",
            "username": "",
            "email": "",
            "activate_code": false,
            "activeusers": []
        }
    }

