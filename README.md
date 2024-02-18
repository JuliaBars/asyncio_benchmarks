***
_Репозиторий на Github [ссылка](https://github.com/JuliaBars/asyncion_benchmarks)_

## RPS для FLask, aiohttp, Starlett

Простое приложение, получающее выборку из БД PostgreSQL.
(Flask использует psycopg2, aiohttp и Starlett asyncpg)

Сначала с помощью asyncpg создадим БД products, заполним ее данными 
и затем протестируем 3 приложения.

Весь код взят из книги "Asyncio и конкурентное программирование на Python" Меттью Фаулера.

**А вот результаты тестов получились совсем не как в книге** :smirk:

_Тесты были запущены на 6-ти ядерном процессоре AMD Ryzen 5 4600H with Radeon Graphics_
_Python 3.10, Debian_

----
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![Flask](https://img.shields.io/badge/FLask-000000?style=for-the-badge&logo=flask&logoColor=white)![aiohttp](https://img.shields.io/badge/aiohttp-2C5BB4?style=for-the-badge&logo=aiohttp)![starlette](https://img.shields.io/badge/starlett-ffff00?style=for-the-badge&Color=white)

___

##### Работа с файлами директории async_db:

1. Запускаем postgres в docker контейнере и соединяем с volume pg_data
```python
>>> docker run --name my-postgres -p 5432:5432 -v pg_data:/var/lib/postgresql/data/ -e POSTGRES_PASSWORD=postgres -d postgres:13.3
```
2. Проверим возможность подключения к БД
```python
>>> python3 connect_to_db_asyncpg.py
```
3. Создадим БД products 
```python
>>> docker exec -ti CONTAINER psql -U postgres -c "CREATE DATABASE products;"
или
>>> python3 0_create_db.py
```
4. Создадим в нашей БД таблицы и наполним их
```python
>>> python3 2_create_tables.py
```
5. Добавим еще несколько строк и получим их из БД
```python
>>> python3 3_insert_select.py 
```
6. Вставим 100 различных брендов в БД, использую список common_words.txt
```python
>>> python3 4_insert_random_brands.py 
```
7. Вставим 999 товаров и SKU в БД
```python
>>> python3 5_insert_goods_and_SKU.py
```
8. Скрипт 6_check_db.py предназначен для отладки, если запросы возвращают None и т.д.

9. Выполнение запросов с помощью пула подключений.
```python
>>> python3 7_create_conn_pull.py
```
10. Выполнение транзакций
```python
успешно:
>>> 8_transaction_success.py
с фейлом:
>>> 8_transaction_failure.py
```
---
##### Измерение RPS приложений:
Будем измерять производительность приложений с помощью утилиты wrk, все они будут выполнять один единственный запрос SELECT brand_id, brand_name FROM brand
1. Установим wrk:
```
>>> apt update
>>> apt install wrk
```
2. Измеряем RPS для приложение на Flask, запускаем приложение на 8 процессах
```
>>> gunicorn -w 8 flask_app:app
```
1 поток, 200 соединений, тестируем 30 секунд:
```
>>> wrk -t1 -c200 -d30s http://127.0.0.1:8000/brands
```
```
Running 30s test @ http://127.0.0.1:8000/brands
  1 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   113.20ms   18.95ms 240.52ms   76.36%
    Req/Sec     1.77k   273.14     2.28k    67.67%
  52918 requests in 30.04s, 214.68MB read
Requests/sec:   1761.30
Transfer/sec:      7.15MB
```

3. Измеряем RPS для приложение на aiohttp в 1м потоке
```
>>> pyhton3 aiohttp_app.py
```
```
>>> wrk -t1 -c200 -d30s http://0.0.0.0:8080/brands
```
```
Running 30s test @ http://0.0.0.0:8080/brands
  1 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   173.95ms  111.50ms   1.22s    72.02%
    Req/Sec     1.21k   241.21     1.74k    71.00%
  36093 requests in 30.05s, 161.12MB read
Requests/sec:   1201.18
Transfer/sec:      5.36MB
```
4. Измеряем RPS для приложения на Starlett на 8ми процессах как и Flask
```
>>> uvicorn --workers 8 --log-level error starlett_app:app
```
```
>>> wrk -t1 -c200 -d30s http://127.0.0.1:8000/brands
```
```
Running 30s test @ http://127.0.0.1:8000/brands
  1 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   145.45ms  105.81ms   1.13s    86.41%
    Req/Sec     1.52k   338.77     2.41k    65.89%
  45286 requests in 30.01s, 182.83MB read
Requests/sec:   1509.00
Transfer/sec:      6.09MB
```

**My Tg [link](https://t.me/JuliaBarss)** :two_hearts:
