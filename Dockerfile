FROM python:3.12-slim

WORKDIR /app-fincancas

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1

RUN pip install --upgrade pip

RUN pip install -r requirements.txt


EXPOSE 8002

RUN docker stop 639e306b76b1 && docker run easypanel/apps/financas:latest

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8002