@echo off
chcp 65001 >nul
echo ============================================================
echo  GemioERP(TM) - 註冊為 Windows 服務
echo  需要 NSSM（Non-Sucking Service Manager）
echo  下載：https://nssm.cc/download
echo ============================================================
echo.

REM 切換至腳本所在目錄
cd /d "%~dp0"

REM 檢查管理員權限
net session >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 請以系統管理員身分執行此腳本！
    pause
    exit /b 1
)

REM 檢查 NSSM 是否存在
where nssm >nul 2>&1
if errorlevel 1 (
    echo [錯誤] 未找到 nssm 指令。
    echo 請下載 NSSM 並將 nssm.exe 加入 PATH，或放至本目錄。
    echo 下載網址：https://nssm.cc/download
    pause
    exit /b 1
)

REM 設定服務名稱與路徑
set SERVICE_NAME=GemioERP
set APP_DIR=%~dp0
set PYTHON=%APP_DIR%venv\Scripts\python.exe
set BACKEND_DIR=%APP_DIR%backend

REM 移除舊服務（若存在）
nssm status %SERVICE_NAME% >nul 2>&1
if not errorlevel 1 (
    echo 移除舊服務...
    nssm stop %SERVICE_NAME% >nul 2>&1
    nssm remove %SERVICE_NAME% confirm >nul 2>&1
)

REM 安裝服務
echo 安裝 Windows 服務：%SERVICE_NAME%...
nssm install %SERVICE_NAME% "%PYTHON%" -m uvicorn main:app --host 0.0.0.0 --port 8090

REM 設定工作目錄
nssm set %SERVICE_NAME% AppDirectory "%BACKEND_DIR%"

REM 設定服務顯示名稱與描述
nssm set %SERVICE_NAME% DisplayName "GemioERP™ Web Server"
nssm set %SERVICE_NAME% Description "GemioERP - Powered by CoreLink AI | Featuring Embedded BI"

REM 設定自動啟動
nssm set %SERVICE_NAME% Start SERVICE_AUTO_START

REM 設定 stdout/stderr 日誌
if not exist "%APP_DIR%logs" mkdir "%APP_DIR%logs"
nssm set %SERVICE_NAME% AppStdout "%APP_DIR%logs\gemio_stdout.log"
nssm set %SERVICE_NAME% AppStderr "%APP_DIR%logs\gemio_stderr.log"
nssm set %SERVICE_NAME% AppRotateFiles 1
nssm set %SERVICE_NAME% AppRotateBytes 10485760

REM 啟動服務
echo 啟動服務...
nssm start %SERVICE_NAME%

echo.
echo ============================================================
echo  服務安裝完成！
echo  服務名稱：%SERVICE_NAME%
echo  存取網址：http://localhost:8090
echo.
echo  管理指令：
echo    啟動：nssm start %SERVICE_NAME%
echo    停止：nssm stop %SERVICE_NAME%
echo    重啟：nssm restart %SERVICE_NAME%
echo    移除：nssm remove %SERVICE_NAME% confirm
echo ============================================================
echo.
pause
