# 注意：此檔案必須最先被執行，確保 i18n 在 model 欄位定義前完成設定。
# Python 匯入 core.globals 時，會先執行本 __init__.py，
# 再執行 globals.py 中的 fastapi_user_auth 匯入。
# model 欄位標籤在 class 定義時即呼叫 i18n()，必須在那之前完成語言設定。

import gettext
from pathlib import Path

# 設定 locale 目錄路徑
_LOCALE_DIR = Path(__file__).parent.parent / "locale"

# 載入繁體中文翻譯（從 .mo 編譯檔）
try:
    _trans = gettext.translation(
        domain="messages",
        localedir=str(_LOCALE_DIR),
        languages=["zh_TW"],
        fallback=True,
    )
    _trans.install()
except Exception:
    pass

# 強制設定 fastapi-amis-admin i18n 語言為繁體中文
# i18n.set_language() 會將所有中文 locale 自動映射為 zh_CN，
# 因此必須直接設定 i18n._language = "zh_TW" 繞過此限制
try:
    from fastapi_amis_admin.utils.translation import i18n
    i18n._language = "zh_TW"
except ImportError:
    try:
        from fastapi_amis_admin import i18n
        i18n._language = "zh_TW"
    except Exception:
        pass
