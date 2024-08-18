FROM python:3

WORKDIR /app

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .

## Выполнение миграций отдельно перед запуском сервера
#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]