<h2>Процесс запуска</h2>
Запустить докер команды
<ol>
    <li><code>docker-compose build</code></li>
    <li><code>docker-compose up</code></li>
</ol>

---
Ссылка на инфо сайт (тут используем cookie и jwt):<br>
https://fastapi-users.github.io/fastapi-users/11.0/configuration/databases/sqlalchemy/

---
В <b>"class User(SQLAlchemyBaseUserTable[int], Base)"</b> в файле <b>"auth/database.py"</b> нельзя просто так удалять поля 
дефолтные. Надо смотреть как сделать можно это. Сейчас просто дописали к ним свои недостающие.

---
<h3>Docker</h3>
Что бы запустить в докере сервер с БД и подключиться к нему с помощью pgadmin4, надо ввести следующие команды:
<ul>
<li> Создать базу данных postgresql через docker: <code>docker run -p 5432:5432 --name pg_trading -e POSTGRES_USER=postgres
  -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:13.3</code></li>
<li> Включить pgAdmin через docker: <code>docker run -e 'PGADMIN_DEFAULT_EMAIL=admin@admin.admin' -e 
  'PGADMIN_DEFAULT_PASSWORD=admin' -d dpage/pgadmin4</code> (При запуске в контейнере ip базы данных сменится!).</li>
</ul>

Перед сборкой надо обязательно создать файл requirements.txt: <code>pip freeze > requirements.txt</code>

Процесс сборки и выполнения приложения в docker:
<ol>
<li><code>docker build . -t fastapi:latest</code> - создание image</li>
<li><code>docker run -d -p 7329:8000 fastapi</code> - запуск (создание контейнера)</li>
<li><code>docker logs 1fe41c00657437bdbe837804a2409267e053ec8b1a5a000c3de8c8f9d1b54f59</code> - проверить на 
наличие ошибок после запуска</li>
</ol>
В п.2 можно задать любой <code>7329</code> НО! <code>8000</code> менять нельзя, тк его указывали ранее. 

---

<h3>Миграции</h3>
<ul>
<li>Если только создали таблицы в проекте - то в начале надо создать директорию 'migrations': <code>alembic init 
migrations</code></li>
<li> Делаем необходимые добавления в файл -> 'migrations/env.py'</li>
<li> Затем создать ревизию: <code>alembic revision --autogenerate -m 'Database Creation'</code></li>
<li> Делаем миграцию (head - до последней, либо версию миграции): <code>alembic upgrage head</code></li>
</ul>
Таблицы должны появиться в БД 

Если потом потребуется откатиться до прошлой версии: <code>alembic downgrage {№ миграции}</code>

---
<h3>Роутеры</h3>
Это переменные, которые аккумулируют в себе какие-то эндпоинты. Если большое приложение и есть много разной логики, 
например, аутентификация пользователя (будет роутер для аутентификации), могут быть роутеры для загрузки/выгрузки 
данных.

---
<h3>Redis</h3>
Это БД (NoSQL). Она хранится в оперативной памяти и имеет формат ключ-значение. Используется для кеширования, хранения 
сессий, ...

Кеширование ответа нашего запроса. <br>
<i>Examples</i>
<ul>
<li><code>keys *</code> - показать все ключи</li>
<li><code>SET server:name "fido"</code> - положить значение "fido" по ключу server:name</li>
<li><code>del server:name</code> - удалить ключ</li>
<li><code>GET server:name</code> => <code>"fido"</code> - получение значения по ключу</li>
<li><code>EXISTS server:name</code> - проверка, есть ли значения по этому ключу</li>
<li><code>EXPIRE server:name 120</code> - через 120 сек ключ server:name будет удален</li>
<li><code>TTL server:name</code> - вывод времени до истечения ключа (-2 - истек; -1 - не истекает)</li>
</ul>
Для запуска redis необходимо запустить сервер (скрипт redis-server). <br>
Для остановки: <code>redis-cli</code> затем <code>shutdown</code>

---
<h3>Celery</h3>
Отдельное приложение. Надо запускать отдельно как uviconr.  
Позволяет делать фоновые задачи, отложенные задачи, периодические задачи (каждый день в 10:00 отправлять отчет 
тем-то). А так же кастомизация этих задач.

Для запуска приложения: <code>celery -A src.tasks.tasks:cel worker --loglevel=INFO</code>

Но перед запуском celery необходимо запустить redis. Редис принимает задачи, хранит их и отдает worker.

!!! Что бы работало через celery, - в функции обязательно написать <code>delay</code>
<br> Пример: <code>sent_email_report.<b>delay</b>(user.username)</code>

---
<h3>Flower</h3>
Графический web-интерфейс для работы. Для отображения celery.  
Работа в интерфейсе с celery и redis. Тут можно увидеть воркеры, активность, таски и тд.

---
<h3>Если запускать все сервисы отдельно</h3>
<ol>
<li>Запустить докер команды по для создания контейнера для БД и pgadmin</li>
    <ul>
        <li> Создать базу данных postgresql через docker: <code>docker run -p 5432:5432 --name pg_trading -e POSTGRES_USER=postgres
          -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:13.3</code></li>
        <li> Включить pgAdmin через docker: <code>docker run -e 'PGADMIN_DEFAULT_EMAIL=admin@admin.admin' -e 
        'PGADMIN_DEFAULT_PASSWORD=admin' -d dpage/pgadmin4</code> (При запуске в контейнере ip базы данных сменится!).</li>
    </ul>
<li>Запустить редис <code>redis-server</code> в терминале</li>
<li>Запустить uvicorn сервер <code>uvicorn src.main:app --reload</code> в терминале</li>
<li>Запустить celery <code>celery -A src.tasks.tasks:cel worker --loglevel=INFO</code> в терминале</li>
<li>Запустить flower <code>celery -A src.tasks.tasks:cel flower</code> в терминале</li>
</ol>