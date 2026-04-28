"""
GemioERP™ - 主程式入口
Powered by CoreLink AI | Featuring Embedded BI

啟動方式（開發）：
    cd backend
    ..\venv\Scripts\python -m uvicorn main:app --host 127.0.0.1 --port 8090
"""

# 重要：必須最先匯入 core，確保 i18n 在 model 定義前設定完成
import core  # noqa: F401

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel

from core.globals import site, auth, auth_engine
from core.init_data import init_data

# 匯入各功能模組的 Admin 類別
from apps.bi.admin import BIApp
from apps.ai.admin import AIApp
from apps.fi.admin import FIApp
from apps.mm.admin import MMApp

# 移除框架預設的 HomeAdmin（由 DashboardAdmin 取代）
from fastapi_amis_admin.admin.site import HomeAdmin
site.unregister_admin(HomeAdmin)

# 向 Admin Site 註冊所有模組
site.register_admin(BIApp, AIApp, FIApp, MMApp)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用程式生命週期管理"""
    # 建立 SQLite auth 資料庫的所有資料表
    async with auth_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # 初始化預設用戶、群組與 casbin 權限
    await init_data()

    yield

    # 關閉資料庫連線池
    await auth_engine.dispose()


# 建立 FastAPI 應用程式
app = FastAPI(
    title="GemioERP™",
    description="Powered by CoreLink AI | Featuring Embedded BI",
    version="1.0.0",
    lifespan=lifespan,
)

# 掛載本機靜態檔案（amis SDK）
_STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")

# 將認證中介軟體加入 admin 子應用（必須在 mount_app 之前）
# 這讓 request.auth 和 request.user 在 admin 路由中可用
site.auth.backend.attach_middleware(site.fastapi)

# 根路徑重導至 admin
@app.get("/")
async def root_redirect():
    return RedirectResponse(url="/admin/")


# 將 Admin Site 掛載至 FastAPI App
site.mount_app(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8090,
        reload=True,
        log_level="info",
    )
