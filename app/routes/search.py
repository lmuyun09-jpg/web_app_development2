"""
Search Routes — 搜尋路由

處理食譜搜尋功能，依關鍵字搜尋食譜名稱與材料。
"""

from flask import Blueprint, render_template, request

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
def search():
    """
    搜尋食譜。

    - GET /search?q=關鍵字

    取得搜尋關鍵字 q，
    若 q 不為空，呼叫 recipe.search(keyword) 搜尋食譜名稱與材料名稱，
    若 q 為空，回傳空結果。
    渲染 search/results.html，傳入 recipes 結果與 keyword。
    """
    pass
