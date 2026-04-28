import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

# 載入環境變數
load_dotenv(Path(__file__).parent.parent / ".env")

from sqlalchemy.ext.asyncio import create_async_engine
from fastapi_amis_admin.admin.settings import Settings
from fastapi_user_auth.admin.site import AuthAdminSite

# ====== 目錄設定 ======
_DATA_DIR = Path(__file__).parent.parent / "data"
_DATA_DIR.mkdir(exist_ok=True)

# ====== Auth 引擎（SQLite，本機儲存）======
auth_engine = create_async_engine(
    f"sqlite+aiosqlite:///{_DATA_DIR}/gemio_auth.db",
    echo=False,
    connect_args={"check_same_thread": False, "timeout": 30},
    pool_size=1,          # SQLite 只允許單一寫入，限制連線池大小
    max_overflow=0,
)


def _build_bi_url() -> str:
    """建立 BI 資料來源（MSSQL）連線字串，自動偵測 ODBC Driver 版本"""
    server = os.getenv("MSSQL_SERVER", "163.17.141.61,8000")
    user = os.getenv("MSSQL_USER", "nutc30")
    password = os.getenv("MSSQL_PASSWORD", "Nutc@2026")
    db = os.getenv("MSSQL_BI_DB", "gemio")

    # 自動偵測 ODBC Driver：優先使用 18，不存在時回退至 17
    driver = "ODBC Driver 18 for SQL Server"
    try:
        import pyodbc
        available = pyodbc.drivers()
        if "ODBC Driver 18 for SQL Server" in available:
            driver = "ODBC Driver 18 for SQL Server"
        elif "ODBC Driver 17 for SQL Server" in available:
            driver = "ODBC Driver 17 for SQL Server"
    except Exception:
        pass

    return (
        f"mssql+aioodbc://{quote_plus(user)}:{quote_plus(password)}"
        f"@{server}/{db}"
        f"?driver={quote_plus(driver)}"
        f"&TrustServerCertificate=yes"
        f"&Encrypt=no"
    )


# ====== BI 引擎（MSSQL，連結 gemio 資料庫）======
# Mac 開發環境若未安裝 unixodbc 則自動回退至 SQLite（唯讀報表頁會顯示無資料）
try:
    bi_engine = create_async_engine(
        _build_bi_url(),
        echo=False,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
except Exception:
    # 無 ODBC 環境（如 macOS 開發機）：回退至 SQLite 避免啟動失敗
    bi_engine = create_async_engine(
        f"sqlite+aiosqlite:///{_DATA_DIR}/gemio_bi_dev.db",
        echo=False,
        connect_args={"check_same_thread": False},
    )

# ====== Admin Site ======
site = AuthAdminSite(
    settings=Settings(
        site_title="GemioERP™",
        site_url=f"http://127.0.0.1:{os.getenv('PORT', '8090')}",
        language="zh_CN",  # 框架基底設定；實際語言由 core/__init__.py 強制覆蓋為 zh_TW
        amis_cdn="/static",  # 使用本機靜態檔案，避免 CDN 速度問題
    ),
    engine=auth_engine,
)

auth = site.auth
