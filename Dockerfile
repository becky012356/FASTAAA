# GemioERP™ - Dockerfile
# 目前以 Win11 本機部署為主；此 Dockerfile 供 Zeabur 雲端部署使用
# Zeabur 部署需在 Variables 設定所有 MSSQL_* 環境變數

FROM python:3.11-slim

# 安裝 MSSQL ODBC Driver 18
RUN apt-get update && apt-get install -y \
    curl gnupg2 apt-transport-https \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/12/prod.list \
       > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製並安裝 Python 依賴
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製後端程式碼
COPY backend/ .

# 建立 data 目錄
RUN mkdir -p data

# 編譯翻譯檔
RUN python locale/compile_mo.py || true

# 開放 Port
EXPOSE 8090

# 啟動指令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8090"]
