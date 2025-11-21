# 改用 slim 版本，體積小非常多，不易崩潰
FROM python:3.10-slim

# 防止 Python 產生 .pyc 檔與緩衝輸出
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 先複製 requirements 以利用 Docker 快取
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Zeabur 會自動注入 PORT，這裡不需要手動 ENV PORT
# 但 CMD 裡面的變數引用是正確的
CMD exec gunicorn --bind 0.0.0.0:$PORT app:app
