"""
MM 採購模組 - 管理介面
- 採購明細表
- 進貨明細表
"""

from fastapi_amis_admin.admin import ModelAdmin, AdminApp
from fastapi_amis_admin.amis.components import PageSchema
from fastapi import Request

from apps.mm.models import PODetail, GRDetail
from core.globals import bi_engine


class PODetailAdmin(ModelAdmin):
    """採購明細表"""
    page_schema = PageSchema(label="採購明細表", icon="fa fa-shopping-cart")
    model = PODetail
    engine = bi_engine  # 使用 MSSQL BI 引擎

    # 列表顯示欄位
    list_display = [
        PODetail.po_no,
        PODetail.po_date,
        PODetail.vendor_code,
        PODetail.vendor_name,
        PODetail.item_code,
        PODetail.item_name,
        PODetail.item_spec,
        PODetail.qty,
        PODetail.unit,
        PODetail.unit_price,
        PODetail.amount,
        PODetail.currency,
        PODetail.po_status,
    ]

    # 搜尋欄位
    search_fields = [
        PODetail.po_no,
        PODetail.vendor_code,
        PODetail.vendor_name,
        PODetail.item_code,
        PODetail.item_name,
    ]

    # 排序
    ordering = [PODetail.po_date.desc()]

    # 唯讀（view 不允許異動）
    async def has_create_permission(self, request: Request, obj=None, data=None) -> bool:
        return False

    async def has_update_permission(self, request: Request, obj=None, data=None) -> bool:
        return False

    async def has_delete_permission(self, request: Request, obj=None, data=None) -> bool:
        return False


class GRDetailAdmin(ModelAdmin):
    """進貨明細表"""
    page_schema = PageSchema(label="進貨明細表", icon="fa fa-truck")
    model = GRDetail
    engine = bi_engine  # 使用 MSSQL BI 引擎

    # 列表顯示欄位
    list_display = [
        GRDetail.gr_no,
        GRDetail.gr_date,
        GRDetail.po_no,
        GRDetail.vendor_code,
        GRDetail.vendor_name,
        GRDetail.item_code,
        GRDetail.item_name,
        GRDetail.item_spec,
        GRDetail.qty,
        GRDetail.unit,
        GRDetail.warehouse_code,
        GRDetail.warehouse_name,
    ]

    # 搜尋欄位
    search_fields = [
        GRDetail.gr_no,
        GRDetail.po_no,
        GRDetail.vendor_code,
        GRDetail.vendor_name,
        GRDetail.item_code,
        GRDetail.item_name,
    ]

    # 排序
    ordering = [GRDetail.gr_date.desc()]

    # 唯讀（view 不允許異動）
    async def has_create_permission(self, request: Request, obj=None, data=None) -> bool:
        return False

    async def has_update_permission(self, request: Request, obj=None, data=None) -> bool:
        return False

    async def has_delete_permission(self, request: Request, obj=None, data=None) -> bool:
        return False


class MMApp(AdminApp):
    """MM 採購模組群組"""
    page_schema = PageSchema(
        label="MM 採購模組",
        icon="fa fa-boxes",
        sort=40,
    )
    router_prefix = "/mm"

    def __init__(self, app=None):
        super().__init__(app)
        self.register_admin(PODetailAdmin, GRDetailAdmin)
