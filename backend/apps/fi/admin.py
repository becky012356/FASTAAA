"""
FI 會計模組 - 管理介面
- 科目餘額表
- 應收明細表
"""

from fastapi_amis_admin.admin import ModelAdmin, AdminApp
from fastapi_amis_admin.amis.components import PageSchema
from fastapi import Request

from apps.fi.models import AccountBalance, ARDetail
from core.globals import bi_engine


class AccountBalanceAdmin(ModelAdmin):
    """科目餘額表"""
    page_schema = PageSchema(label="科目餘額表", icon="fa fa-balance-scale")
    model = AccountBalance
    engine = bi_engine  # 使用 MSSQL BI 引擎

    # 列表顯示欄位
    list_display = [
        AccountBalance.acct_code,
        AccountBalance.acct_name,
        AccountBalance.fiscal_year,
        AccountBalance.period,
        AccountBalance.begin_balance,
        AccountBalance.debit_amount,
        AccountBalance.credit_amount,
        AccountBalance.end_balance,
        AccountBalance.currency,
    ]

    # 搜尋欄位
    search_fields = [
        AccountBalance.acct_code,
        AccountBalance.acct_name,
        AccountBalance.fiscal_year,
        AccountBalance.period,
    ]

    # 排序
    ordering = [AccountBalance.acct_code]

    # 唯讀（view 不允許異動）
    async def has_create_permission(self, request: Request, obj=None, data=None) -> bool:
        return False

    async def has_update_permission(self, request: Request, obj=None, data=None) -> bool:
        return False

    async def has_delete_permission(self, request: Request, obj=None, data=None) -> bool:
        return False


class ARDetailAdmin(ModelAdmin):
    """應收明細表"""
    page_schema = PageSchema(label="應收明細表", icon="fa fa-file-invoice-dollar")
    model = ARDetail
    engine = bi_engine  # 使用 MSSQL BI 引擎

    # 列表顯示欄位
    list_display = [
        ARDetail.cust_code,
        ARDetail.cust_name,
        ARDetail.doc_no,
        ARDetail.doc_date,
        ARDetail.due_date,
        ARDetail.amount,
        ARDetail.unpaid_amount,
        ARDetail.currency,
        ARDetail.remark,
    ]

    # 搜尋欄位
    search_fields = [
        ARDetail.cust_code,
        ARDetail.cust_name,
        ARDetail.doc_no,
    ]

    # 排序
    ordering = [ARDetail.doc_date.desc()]

    # 唯讀（view 不允許異動）
    async def has_create_permission(self, request: Request, obj=None, data=None) -> bool:
        return False

    async def has_update_permission(self, request: Request, obj=None, data=None) -> bool:
        return False

    async def has_delete_permission(self, request: Request, obj=None, data=None) -> bool:
        return False


class FIApp(AdminApp):
    """FI 會計模組群組"""
    page_schema = PageSchema(
        label="FI 會計模組",
        icon="fa fa-calculator",
        sort=30,
    )
    router_prefix = "/fi"

    def __init__(self, app=None):
        super().__init__(app)
        self.register_admin(AccountBalanceAdmin, ARDetailAdmin)
