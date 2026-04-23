"""
Step Routes — 步驟路由

處理步驟的新增、編輯、刪除與排序操作。
所有操作完成後重導向到食譜詳情頁。
"""

from flask import Blueprint, request, redirect, url_for, abort, current_app, flash
from app.models import step

step_bp = Blueprint('step', __name__)


@step_bp.route('/recipes/<int:id>/steps', methods=['POST'])
def create(id):
    """
    新增步驟。
    """
    description = request.form.get('description', '').strip()
    
    if not description:
        flash('步驟內容為必填', 'error')
        return redirect(url_for('recipe.detail', id=id))

    db_path = current_app.config['DATABASE']
    step.create(db_path, id, description)
    flash('新增步驟成功！', 'success')
    return redirect(url_for('recipe.detail', id=id))


@step_bp.route('/recipes/<int:id>/steps/<int:step_id>/edit', methods=['POST'])
def update(id, step_id):
    """
    編輯步驟。
    """
    db_path = current_app.config['DATABASE']
    s = step.get_by_id(db_path, step_id)
    if not s or s['recipe_id'] != id:
        abort(404)
        
    description = request.form.get('description', '').strip()
    if not description:
        flash('步驟內容為必填', 'error')
        return redirect(url_for('recipe.detail', id=id))

    step.update(db_path, step_id, description)
    flash('步驟更新成功！', 'success')
    return redirect(url_for('recipe.detail', id=id))


@step_bp.route('/recipes/<int:id>/steps/<int:step_id>/delete', methods=['POST'])
def delete(id, step_id):
    """
    刪除步驟。
    """
    db_path = current_app.config['DATABASE']
    s = step.get_by_id(db_path, step_id)
    if not s or s['recipe_id'] != id:
        abort(404)
        
    step.delete(db_path, step_id)
    flash('步驟已刪除', 'success')
    return redirect(url_for('recipe.detail', id=id))


@step_bp.route('/recipes/<int:id>/steps/<int:step_id>/move-up', methods=['POST'])
def move_up(id, step_id):
    """
    步驟上移。
    """
    db_path = current_app.config['DATABASE']
    s = step.get_by_id(db_path, step_id)
    if not s or s['recipe_id'] != id:
        abort(404)
        
    step.move_up(db_path, step_id)
    return redirect(url_for('recipe.detail', id=id))


@step_bp.route('/recipes/<int:id>/steps/<int:step_id>/move-down', methods=['POST'])
def move_down(id, step_id):
    """
    步驟下移。
    """
    db_path = current_app.config['DATABASE']
    s = step.get_by_id(db_path, step_id)
    if not s or s['recipe_id'] != id:
        abort(404)
        
    step.move_down(db_path, step_id)
    return redirect(url_for('recipe.detail', id=id))
