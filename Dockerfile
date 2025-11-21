# 使用 Python 3.10 完整版 (非 slim)，確保 extract-msg 底層依賴 (如 olefile) 能順利運作
FROM python:3.10

# 設定工作目錄
WORKDIR /app

# 設定環境變數
# PYTHONUNBUFFERED=1: 讓 Python 的 Log 直接輸出到 Console，方便在 Zeabur Dashboard 查看
# PYTHONDONTWRITEBYTECODE=1: 防止產生 .pyc 檔案
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有程式碼到容器中
COPY . .

# 宣告容器將使用的 Port (僅供文件參考，實際綁定由 CMD 決定)
EXPOSE 8080

# 啟動指令
# 使用 gunicorn 作為 WSGI Server
# --bind 0.0.0.0:$PORT : 讓 Zeabur 動態注入 PORT 環境變數
# app:app : 對應 app.py 中的 app 物件
CMD gunicorn --bind 0.0.0.0:${PORT:-8080} app:app
