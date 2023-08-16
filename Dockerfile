# Развертывание только fastapi (только 1 приложение можно развернить так)
# RUN прогоняется только при сборке образа, а когда запустим его (контейнер) - тогда запустится команда CMD

# СБОРКА ОБРАЗА
FROM python:3.9

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /fastapi_app

RUN chmod a+x docker/*.sh

#WORKDIR /src
# ЗАВЕРШЕНИЕ СБОРКАРКИ ОБРАЗА

#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
