"""
Recipe Routes — 食譜路由

處理食譜的 CRUD 操作：列表、新增、詳情、編輯、刪除。
"""

from flask import Blueprint, render_template, request, redirect, url_for, abort

recipe_bp = Blueprint('recipe', __name__)


@recipe_bp.route('/')
@recipe_bp.route('/recipes')
def index():
    """
    食譜列表頁。

    - GET /
    - GET /recipes
    - GET /recipes?category=中式

    顯示所有食譜，支援依分類篩選。
    呼叫 recipe.get_all()，渲染 index.html。
    """
    pass


@recipe_bp.route('/recipes/create', methods=['GET'])
def create_form():
    """
    新增食譜表單頁面。

    - GET /recipes/create

    顯示空白的新增食譜表單。
    呼叫 recipe.get_categories()，渲染 recipe/create.html。
    """
    pass


@recipe_bp.route('/recipes/create', methods=['POST'])
def create():
    """
    建立食譜。

    - POST /recipes/create

    接收表單資料（name, description, category, cooking_time, servings），
    驗證 name 不為空，呼叫 recipe.create()，
    重導向到 /recipes/<new_id>。
    """
    pass


@recipe_bp.route('/recipes/<int:id>')
def detail(id):
    """
    食譜詳情頁。

    - GET /recipes/<id>

    顯示食譜完整資訊，包含材料清單與步驟清單。
    呼叫 recipe.get_by_id()、ingredient.get_by_recipe_id()、step.get_by_recipe_id()，
    渲染 recipe/detail.html。
    找不到食譜時回傳 404。
    """
    pass


@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_form(id):
    """
    編輯食譜表單頁面。

    - GET /recipes/<id>/edit

    顯示已填入現有資料的編輯表單。
    呼叫 recipe.get_by_id() 與 recipe.get_categories()，
    渲染 recipe/edit.html。
    找不到食譜時回傳 404。
    """
    pass


@recipe_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update(id):
    """
    更新食譜。

    - POST /recipes/<id>/edit

    接收表單資料，驗證 name 不為空，
    呼叫 recipe.update()，重導向到 /recipes/<id>。
    找不到食譜時回傳 404。
    """
    pass


@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除食譜。

    - POST /recipes/<id>/delete

    呼叫 recipe.delete()（CASCADE 自動刪除材料與步驟），
    重導向到 /recipes。
    找不到食譜時回傳 404。
    """
    pass
