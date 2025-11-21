FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 第一處修正：注意最後面有一個點
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 第二處修正：注意最後面有一個點
COPY app.py .

ENV PORT=8080

CMD exec gunicorn --bind 0.0.0.0:${PORT} app:app
