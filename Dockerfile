FROM python:3.10

ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -y postgresql postgresql-contrib


WORKDIR /app

COPY ./src /app

COPY ./requirements.txt /app

RUN pip install -r /app/requirements.txt


RUN service postgresql start \
    && su postgres -c "psql -c 'CREATE DATABASE SPECTR_ANALIZER;'" \
    && su postgres -c "psql -c 'CREATE USER postrgresql WITH PASSWORD '\''1234'\'';'" \
    && su postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE SPECTR_ANALIZER TO postrgresql;'"

# Запуск команды приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]