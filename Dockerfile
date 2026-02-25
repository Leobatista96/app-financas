FROM python:3.12-slim

WORKDIR /app-fincancas

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1

RUN pip install --upgrade pip

RUN pip install -r requirements.txt


EXPOSE 8002

CMD python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic && python manage.py runserver 0.0.0.0:8002