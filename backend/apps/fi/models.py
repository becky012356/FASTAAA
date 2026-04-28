"""
FI 會計模組 - 資料模型
對應 gemio 資料庫的 view，欄位定義請依實際 view schema 調整
"""

from typing import Optional
from datetime import date
from decimal import Decimal

from sqlmodel import SQLModel, Field


class AccountBalance(SQLModel, table=True):
    """科目餘額表 - 對應 gemio 資料庫 view"""
    __tablename__ = "v_fi_account_balance"  # 請修改為實際 view 名稱
    __table_args__ = {"extend_existing": True}

    # 主鍵欄位（請依實際 view 主鍵調整）
    id: Optional[int] = Field(default=None, primary_key=True)

    # 科目資訊
    acct_code: Optional[str] = Field(default=None, title="科目代碼", max_length=20)
    acct_name: Optional[str] = Field(default=None, title="科目名稱", max_length=100)

    # 期間
    fiscal_year: Optional[str] = Field(default=None, title="會計年度", max_length=4)
    period: Optional[str] = Field(default=None, title="期間", max_length=2)

    # 金額
    begin_balance: Optional[Decimal] = Field(default=None, title="期初餘額")
    debit_amount: Optional[Decimal] = Field(default=None, title="借方發生額")
    credit_amount: Optional[Decimal] = Field(default=None, title="貸方發生額")
    end_balance: Optional[Decimal] = Field(default=None, title="期末餘額")

    # 幣別
    currency: Optional[str] = Field(default=None, title="幣別", max_length=5)


class ARDetail(SQLModel, table=True):
    """應收明細表 - 對應 gemio 資料庫 view"""
    __tablename__ = "v_fi_ar_detail"  # 請修改為實際 view 名稱
    __table_args__ = {"extend_existing": True}

    # 主鍵欄位（請依實際 view 主鍵調整）
    id: Optional[int] = Field(default=None, primary_key=True)

    # 客戶資訊
    cust_code: Optional[str] = Field(default=None, title="客戶代碼", max_length=20)
    cust_name: Optional[str] = Field(default=None, title="客戶名稱", max_length=100)

    # 憑證資訊
    doc_no: Optional[str] = Field(default=None, title="憑證號碼", max_length=30)
    doc_date: Optional[date] = Field(default=None, title="交易日期")
    due_date: Optional[date] = Field(default=None, title="到期日")

    # 金額
    amount: Optional[Decimal] = Field(default=None, title="交易金額")
    unpaid_amount: Optional[Decimal] = Field(default=None, title="未收金額")
    currency: Optional[str] = Field(default=None, title="幣別", max_length=5)

    # 備註
    remark: Optional[str] = Field(default=None, title="備註", max_length=200)
