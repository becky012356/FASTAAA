"""
MM 採購模組 - 資料模型
對應 gemio 資料庫的 view，欄位定義請依實際 view schema 調整
"""

from typing import Optional
from datetime import date
from decimal import Decimal

from sqlmodel import SQLModel, Field


class PODetail(SQLModel, table=True):
    """採購明細表 - 對應 gemio 資料庫 view"""
    __tablename__ = "v_mm_po_detail"  # 請修改為實際 view 名稱
    __table_args__ = {"extend_existing": True}

    # 主鍵欄位（請依實際 view 主鍵調整）
    id: Optional[int] = Field(default=None, primary_key=True)

    # 採購單資訊
    po_no: Optional[str] = Field(default=None, title="採購單號", max_length=30)
    po_date: Optional[date] = Field(default=None, title="採購日期")
    po_status: Optional[str] = Field(default=None, title="狀態", max_length=20)

    # 廠商資訊
    vendor_code: Optional[str] = Field(default=None, title="廠商代碼", max_length=20)
    vendor_name: Optional[str] = Field(default=None, title="廠商名稱", max_length=100)

    # 物料資訊
    item_code: Optional[str] = Field(default=None, title="物料代碼", max_length=30)
    item_name: Optional[str] = Field(default=None, title="物料名稱", max_length=100)
    item_spec: Optional[str] = Field(default=None, title="規格", max_length=200)

    # 數量與金額
    qty: Optional[Decimal] = Field(default=None, title="採購數量")
    unit: Optional[str] = Field(default=None, title="單位", max_length=10)
    unit_price: Optional[Decimal] = Field(default=None, title="單價")
    amount: Optional[Decimal] = Field(default=None, title="採購金額")
    currency: Optional[str] = Field(default=None, title="幣別", max_length=5)

    # 備註
    remark: Optional[str] = Field(default=None, title="備註", max_length=200)


class GRDetail(SQLModel, table=True):
    """進貨明細表 - 對應 gemio 資料庫 view"""
    __tablename__ = "v_mm_gr_detail"  # 請修改為實際 view 名稱
    __table_args__ = {"extend_existing": True}

    # 主鍵欄位（請依實際 view 主鍵調整）
    id: Optional[int] = Field(default=None, primary_key=True)

    # 進貨單資訊
    gr_no: Optional[str] = Field(default=None, title="進貨單號", max_length=30)
    gr_date: Optional[date] = Field(default=None, title="進貨日期")
    po_no: Optional[str] = Field(default=None, title="採購單號", max_length=30)

    # 廠商資訊
    vendor_code: Optional[str] = Field(default=None, title="廠商代碼", max_length=20)
    vendor_name: Optional[str] = Field(default=None, title="廠商名稱", max_length=100)

    # 物料資訊
    item_code: Optional[str] = Field(default=None, title="物料代碼", max_length=30)
    item_name: Optional[str] = Field(default=None, title="物料名稱", max_length=100)
    item_spec: Optional[str] = Field(default=None, title="規格", max_length=200)

    # 數量資訊
    qty: Optional[Decimal] = Field(default=None, title="進貨數量")
    unit: Optional[str] = Field(default=None, title="單位", max_length=10)

    # 倉庫
    warehouse_code: Optional[str] = Field(default=None, title="倉庫代碼", max_length=10)
    warehouse_name: Optional[str] = Field(default=None, title="倉庫名稱", max_length=50)

    # 備註
    remark: Optional[str] = Field(default=None, title="備註", max_length=200)
