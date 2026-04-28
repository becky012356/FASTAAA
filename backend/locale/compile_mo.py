"""
編譯 .po 翻譯檔為 .mo 二進位格式
修改 messages.po 後執行本腳本以更新翻譯
使用方式：python locale/compile_mo.py
"""

import subprocess
import sys
from pathlib import Path

PO_FILE = Path(__file__).parent / "zh_TW" / "LC_MESSAGES" / "messages.po"
MO_FILE = PO_FILE.with_suffix(".mo")


def compile_po():
    # 方式一：使用系統的 msgfmt 工具（需安裝 gettext）
    try:
        result = subprocess.run(
            ["msgfmt", "-o", str(MO_FILE), str(PO_FILE)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"編譯成功：{MO_FILE}")
            return True
        else:
            print(f"msgfmt 錯誤：{result.stderr}")
    except FileNotFoundError:
        print("未找到 msgfmt，嘗試使用 Babel...")

    # 方式二：使用 Babel（Python 套件）
    try:
        from babel.messages.mofile import write_mo
        from babel.messages.pofile import read_po

        with open(PO_FILE, "rb") as f:
            catalog = read_po(f)

        with open(MO_FILE, "wb") as f:
            write_mo(f, catalog)

        print(f"編譯成功（Babel）：{MO_FILE}")
        return True

    except ImportError:
        print("請安裝 Babel：pip install Babel")
    except Exception as e:
        print(f"Babel 編譯失敗：{e}")

    return False


if __name__ == "__main__":
    success = compile_po()
    sys.exit(0 if success else 1)
