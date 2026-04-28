"""
BI 商業智慧模組
- 儀表板（歡迎頁）
"""

from fastapi_amis_admin.admin import PageAdmin
from fastapi_amis_admin.amis.components import Page, PageSchema, Html, Grid, Panel
from fastapi import Request


class DashboardAdmin(PageAdmin):
    """儀表板首頁"""
    page_schema = PageSchema(
        label="儀表板",
        icon="fa fa-home",
        sort=10,
    )

    async def get_page(self, request: Request) -> Page:
        return Page(
            title="",
            body=Html(html="""
<div style="padding: 40px; text-align: center; font-family: 'Microsoft JhengHei', sans-serif;">
  <div style="margin-bottom: 32px;">
    <h1 style="font-size: 2.8rem; font-weight: 700; color: #1a1a2e; margin: 0;">
      GemioERP<sup style="font-size:1.2rem;">&#8482;</sup>
    </h1>
    <p style="font-size: 1.1rem; color: #4a5568; margin-top: 8px; letter-spacing: 0.05em;">
      Powered by CoreLink AI &nbsp;|&nbsp; Featuring Embedded BI
    </p>
  </div>

  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
              gap: 24px; max-width: 960px; margin: 0 auto 40px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px; padding: 28px 20px; color: white;">
      <div style="font-size: 2rem; margin-bottom: 8px;">&#128202;</div>
      <div style="font-size: 1.2rem; font-weight: 600;">FI 會計模組</div>
      <div style="font-size: 0.9rem; opacity: 0.85; margin-top: 4px;">科目餘額 | 應收明細</div>
    </div>
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 12px; padding: 28px 20px; color: white;">
      <div style="font-size: 2rem; margin-bottom: 8px;">&#128230;</div>
      <div style="font-size: 1.2rem; font-weight: 600;">MM 採購模組</div>
      <div style="font-size: 0.9rem; opacity: 0.85; margin-top: 4px;">採購明細 | 進貨明細</div>
    </div>
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                border-radius: 12px; padding: 28px 20px; color: white;">
      <div style="font-size: 2rem; margin-bottom: 8px;">&#129302;</div>
      <div style="font-size: 1.2rem; font-weight: 600;">AI 智慧分析</div>
      <div style="font-size: 0.9rem; opacity: 0.85; margin-top: 4px;">即將推出</div>
    </div>
  </div>

  <div style="background: #f8f9fa; border-radius: 12px; padding: 24px;
              max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0;">
    <p style="color: #718096; font-size: 0.95rem; margin: 0; line-height: 1.8;">
      本系統連結現有 ERP SQL Server，提供 BI 分析與 AI 智慧分析功能，<br>
      補足舊有 ERP 功能不足，擔任公司數據中台角色。
    </p>
  </div>
</div>
"""),
        )


# 對外匯出，供 main.py 使用 AdminApp 群組
class BIApp:
    """BI 商業智慧模組 - 使用 AdminApp 包裝"""
    pass


# 為了讓 main.py 可以直接 register_admin，將 DashboardAdmin 作為 BIApp
BIApp = DashboardAdmin
