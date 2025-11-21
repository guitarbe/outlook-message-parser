FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PORT=8080

CMD exec gunicorn --bind 0.0.0.0:${PORT} app:app
