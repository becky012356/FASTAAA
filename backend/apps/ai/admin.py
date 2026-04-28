"""
AI 智慧分析模組
- 分析頁（即將推出）
"""

from fastapi_amis_admin.admin import PageAdmin
from fastapi_amis_admin.amis.components import Page, PageSchema, Html
from fastapi import Request


class AIAnalysisAdmin(PageAdmin):
    """AI 智慧分析頁"""
    page_schema = PageSchema(
        label="AI 智慧分析",
        icon="fa fa-robot",
        sort=20,
    )

    async def get_page(self, request: Request) -> Page:
        return Page(
            title="AI 智慧分析",
            body=Html(html="""
<div style="padding: 60px 40px; text-align: center;
            font-family: 'Microsoft JhengHei', sans-serif;">
  <div style="font-size: 4rem; margin-bottom: 16px;">&#129302;</div>
  <h2 style="font-size: 1.8rem; color: #2d3748; margin: 0 0 12px;">
    AI 智慧分析
  </h2>
  <p style="color: #718096; font-size: 1rem; margin-bottom: 32px;">
    Powered by CoreLink AI
  </p>
  <div style="display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2);
              color: white; border-radius: 24px; padding: 10px 32px;
              font-size: 1rem; font-weight: 600; letter-spacing: 0.08em;">
    即將推出
  </div>
  <p style="color: #a0aec0; font-size: 0.85rem; margin-top: 24px;">
    本模組將整合 CoreLink AI 引擎，提供智慧財務分析、採購預測與異常偵測功能。
  </p>
</div>
"""),
        )


# 對外匯出
AIApp = AIAnalysisAdmin
