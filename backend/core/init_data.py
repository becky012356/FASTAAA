"""
初始資料建立模組
- 建立 root 超級管理員的 casbin policy（必要！否則 root 無法登入）
- 建立系統用戶群組（co, fi, mm, sd, pp, wm）
- 建立預設用戶帳號（所有預設密碼：123456）
"""

from sqlmodel import Session, select

from core.globals import auth


def _init_sync(session: Session):
    """同步初始化函式，透過 async_run_sync 執行以避免 SQLite 鎖定衝突"""
    from fastapi_user_auth.auth.models import CasbinRule, Role, User
    from casbin import AsyncEnforcer

    # ── 1. 建立 root 角色與用戶 ──────────────────────────────────────
    from sqlmodel import select
    role = session.scalar(select(Role).where(Role.key == "root"))
    if not role:
        role = Role(key="root", name="root role")
        session.add(role)
        session.flush()

    user = session.scalar(select(User).where(User.username == "nutc30"))
    if not user:
        user = User(
            username="nutc30",
            password=auth.pwd_context.hash("root"),
        )
        session.add(user)
        session.flush()

    # nutc30 的角色指派規則
    g_rule = session.scalar(
        select(CasbinRule).where(
            CasbinRule.ptype == "g",
            CasbinRule.v0 == "u:nutc30",
            CasbinRule.v1 == "r:root",
        )
    )
    if not g_rule:
        session.add(CasbinRule(ptype="g", v0="u:nutc30", v1="r:root"))
        session.flush()

    # ── 2. 建立 root 的 casbin policy（允許存取所有頁面）─────────────
    p_rule = session.scalar(
        select(CasbinRule).where(
            CasbinRule.ptype == "p",
            CasbinRule.v0 == "r:root",
            CasbinRule.v4 == "allow",
        )
    )
    if not p_rule:
        session.add(CasbinRule(
            ptype="p",
            v0="r:root",   # sub：role root
            v1="*",        # obj：所有資源
            v2="page",     # act：page 動作
            v3="page",     # group：page 群組
            v4="allow",    # eft：允許
        ))
        session.flush()

    # ── 3. 建立各部門群組 ─────────────────────────────────────────────
    groups = {
        "co": "總公司（全模組）",
        "fi": "會計部門",
        "mm": "採購部門",
        "sd": "業務部門",
        "pp": "生產部門",
        "wm": "倉庫部門",
    }
    for code, label in groups.items():
        existing = session.scalar(select(Role).where(Role.key == f"usergroup:{code}"))
        if not existing:
            session.add(Role(key=f"usergroup:{code}", name=label))
    session.flush()

    # ── 4. 建立各部門預設用戶（密碼：123456）─────────────────────────
    users_config = {
        "co01": ["co"],
        "fi01": ["fi"],
        "mm01": ["mm"],
        "sd01": ["sd"],
        "pp01": ["pp"],
        "wm01": ["wm"],
    }
    for username, user_groups in users_config.items():
        existing_user = session.scalar(select(User).where(User.username == username))
        if not existing_user:
            new_user = User(
                username=username,
                password=auth.pwd_context.hash("123456"),
                email=f"{username}@gemio.local",
            )
            session.add(new_user)
            session.flush()

            for group_code in user_groups:
                existing_grule = session.scalar(
                    select(CasbinRule).where(
                        CasbinRule.ptype == "g",
                        CasbinRule.v0 == f"u:{username}",
                        CasbinRule.v1 == f"r:usergroup:{group_code}",
                    )
                )
                if not existing_grule:
                    session.add(CasbinRule(
                        ptype="g",
                        v0=f"u:{username}",
                        v1=f"r:usergroup:{group_code}",
                    ))
    session.flush()
    session.commit()


async def init_data():
    """啟動時初始化資料（使用 async_run_sync 確保單一連線）"""
    try:
        await auth.db.async_run_sync(_init_sync)
        # 重新載入 casbin enforcer 使新規則生效
        await auth.enforcer.load_policy()
    except Exception as e:
        # 初始化失敗不阻止系統啟動（資料可能已存在）
        import traceback
        traceback.print_exc()
