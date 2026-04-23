"""
Ingredient Routes — 材料路由

處理材料的新增、編輯、刪除操作。
所有操作完成後重導向到食譜詳情頁。
"""

from flask import Blueprint, request, redirect, url_for, abort, current_app, flash
from app.models import ingredient

ingredient_bp = Blueprint('ingredient', __name__)


@ingredient_bp.route('/recipes/<int:id>/ingredients', methods=['POST'])
def create(id):
    """
    新增材料。
    """
    name = request.form.get('name', '').strip()
    amount = request.form.get('amount', '').strip()
    unit = request.form.get('unit', '').strip()
    
    if not name:
        flash('材料名稱為必填', 'error')
        return redirect(url_for('recipe.detail', id=id))

    db_path = current_app.config['DATABASE']
    ingredient.create(db_path, id, name, amount, unit)
    flash('新增材料成功！', 'success')
    return redirect(url_for('recipe.detail', id=id))


@ingredient_bp.route('/recipes/<int:id>/ingredients/<int:ing_id>/edit', methods=['POST'])
def update(id, ing_id):
    """
    編輯材料。
    """
    db_path = current_app.config['DATABASE']
    ing = ingredient.get_by_id(db_path, ing_id)
    if not ing or ing['recipe_id'] != id:
        abort(404)
        
    name = request.form.get('name', '').strip()
    amount = request.form.get('amount', '').strip()
    unit = request.form.get('unit', '').strip()

    if not name:
        flash('材料名稱為必填', 'error')
        return redirect(url_for('recipe.detail', id=id))

    ingredient.update(db_path, ing_id, name, amount, unit)
    flash('材料更新成功！', 'success')
    return redirect(url_for('recipe.detail', id=id))


@ingredient_bp.route('/recipes/<int:id>/ingredients/<int:ing_id>/delete', methods=['POST'])
def delete(id, ing_id):
    """
    刪除材料。
    """
    db_path = current_app.config['DATABASE']
    ing = ingredient.get_by_id(db_path, ing_id)
    if not ing or ing['recipe_id'] != id:
        abort(404)
        
    ingredient.delete(db_path, ing_id)
    flash('材料已刪除', 'success')
    return redirect(url_for('recipe.detail', id=id))
