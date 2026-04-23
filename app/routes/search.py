"""
Search Routes — 搜尋路由

處理食譜搜尋功能，依關鍵字搜尋食譜名稱與材料。
"""

from flask import Blueprint, render_template, request, current_app
from app.models import recipe

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
def search():
    """
    搜尋食譜。
    """
    keyword = request.args.get('q', '').strip()
    recipes = []
    
    if keyword:
        db_path = current_app.config['DATABASE']
        recipes = recipe.search(db_path, keyword)
    
    return render_template('search/results.html', recipes=recipes, keyword=keyword)
