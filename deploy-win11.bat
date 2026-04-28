@echo off
chcp 65001 >nul
echo ============================================================
echo  GemioERP(TM) - Win11 一鍵部署腳本
echo  Powered by CoreLink AI ^| Featuring Embedded BI
echo ============================================================
echo.

REM 切換至腳本所在目錄
cd /d "%~dp0"

REM ── 步驟 1：建立虛擬環境 ──────────────────────────────────────
echo [1/5] 建立 Python 虛擬環境...
if exist venv (
    echo   虛擬環境已存在，略過建立。
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [錯誤] 建立虛擬環境失敗，請確認已安裝 Python 3.10+
        pause
        exit /b 1
    )
    echo   虛擬環境建立完成。
)

REM ── 步驟 2：安裝依賴套件 ─────────────────────────────────────
echo.
echo [2/5] 安裝依賴套件...
venv\Scripts\pip install --upgrade pip -q
venv\Scripts\pip install -r backend\requirements.txt
if errorlevel 1 (
    echo [錯誤] 套件安裝失敗，請檢查 requirements.txt
    pause
    exit /b 1
)
echo   套件安裝完成。

REM ── 步驟 3：編譯繁體中文翻譯 ────────────────────────────────
echo.
echo [3/5] 編譯繁體中文翻譯檔...
venv\Scripts\python backend\locale\compile_mo.py
if errorlevel 1 (
    echo [警告] 翻譯編譯失敗，系統將以預設語言運行。
) else (
    echo   翻譯編譯完成。
)

REM ── 步驟 4：建立 data 目錄 ──────────────────────────────────
echo.
echo [4/5] 建立資料目錄...
if not exist backend\data mkdir backend\data
echo   資料目錄就緒。

REM ── 步驟 5：開放防火牆 Port 8090 ────────────────────────────
echo.
echo [5/5] 設定防火牆規則（Port 8090）...
netsh advfirewall firewall show rule name="GemioERP" >nul 2>&1
if errorlevel 1 (
    netsh advfirewall firewall add rule name="GemioERP" dir=in action=allow protocol=TCP localport=8090
    echo   防火牆規則已新增。
) else (
    echo   防火牆規則已存在，略過。
)

echo.
echo ============================================================
echo  部署完成！
echo  啟動指令：
echo    cd backend
echo    ..\venv\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 8090
echo ============================================================
echo.
pause
