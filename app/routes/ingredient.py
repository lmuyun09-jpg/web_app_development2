"""
Ingredient Routes — 材料路由

處理材料的新增、編輯、刪除操作。
所有操作完成後重導向到食譜詳情頁。
"""

from flask import Blueprint, request, redirect, url_for, abort

ingredient_bp = Blueprint('ingredient', __name__)


@ingredient_bp.route('/recipes/<int:id>/ingredients', methods=['POST'])
def create(id):
    """
    新增材料。

    - POST /recipes/<id>/ingredients

    接收表單資料（name, amount, unit），
    驗證 name 不為空，呼叫 ingredient.create()，
    重導向到 /recipes/<id>。
    """
    pass


@ingredient_bp.route('/recipes/<int:id>/ingredients/<int:ing_id>/edit', methods=['POST'])
def update(id, ing_id):
    """
    編輯材料。

    - POST /recipes/<id>/ingredients/<ing_id>/edit

    接收表單資料（name, amount, unit），
    驗證 name 不為空，呼叫 ingredient.update()，
    重導向到 /recipes/<id>。
    找不到材料時回傳 404。
    """
    pass


@ingredient_bp.route('/recipes/<int:id>/ingredients/<int:ing_id>/delete', methods=['POST'])
def delete(id, ing_id):
    """
    刪除材料。

    - POST /recipes/<id>/ingredients/<ing_id>/delete

    呼叫 ingredient.delete()，重導向到 /recipes/<id>。
    找不到材料時回傳 404。
    """
    pass
