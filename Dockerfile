FROM python:3.10

# 設定工作目錄
WORKDIR /app

# 一次將所有檔案複製進去 (這通常比一行一行複製不容易出錯)
COPY . .

# 安裝套件
RUN pip install --upgrade pip && pip install -r requirements.txt

# 設定環境變數
ENV PORT=8080

# 啟動服務
CMD exec gunicorn --bind 0.0.0.0:${PORT} app:app
