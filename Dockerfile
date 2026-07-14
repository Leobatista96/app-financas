FROM python:3.12-slim

WORKDIR /app-fincancas

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1

RUN pip install --upgrade pip

RUN pip install -r requirements.txt


EXPOSE 8002

CMD python manage.py migrate && python manage.py collectstatic --noinput && python -m gunicorn app.wsgi:application --bind 0.0.0.0:8002 && celery -A app worker -l INFO
