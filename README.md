# Bottec - тестовое задание

### Разворачивание проекта

Возможно двумя путями: локальноxthtp Poetry и через Docker Compose:

#### Через Docker Compose

```
    cd path/to/the/project
    docker-compose up
```

#### Локально через Poetry
```
    psql postgres
     create database bottec_test;
     exit;
 
    cd path/to/the/project
    cp dev.env .env

    poetry install
    poetry run alembic upgrade head
```

##### Запуск сервиса для обновления данных из API:
```
./currency_update.sh
```

##### Запуск API (в другой вкладке консоли):
```
./api.sh
```

### Запуск тестов (в развернутом окружении):
```
pytest
```


### Ссылки на API и Swagger

 - **API:** <http://127.0.0.1:8000>
 - **Swagger:** <http://127.0.0.1:8000/docs/>

