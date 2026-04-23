"""
Recipe Routes — 食譜路由

處理食譜的 CRUD 操作：列表、新增、詳情、編輯、刪除。
"""

from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app, flash
from app.models import recipe, ingredient, step

recipe_bp = Blueprint('recipe', __name__)


@recipe_bp.route('/')
@recipe_bp.route('/recipes')
def index():
    """
    食譜列表頁。
    顯示所有食譜，支援依分類篩選。
    """
    category = request.args.get('category')
    db_path = current_app.config['DATABASE']
    
    recipes = recipe.get_all(db_path, category=category)
    categories = recipe.get_categories()
    
    return render_template('index.html', recipes=recipes, categories=categories, current_category=category)


@recipe_bp.route('/recipes/create', methods=['GET'])
def create_form():
    """
    新增食譜表單頁面。
    """
    categories = recipe.get_categories()
    return render_template('recipe/create.html', categories=categories)


@recipe_bp.route('/recipes/create', methods=['POST'])
def create():
    """
    建立食譜。
    """
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', '其他')
    cooking_time = request.form.get('cooking_time')
    servings = request.form.get('servings')

    if not name:
        flash('食譜名稱為必填', 'error')
        categories = recipe.get_categories()
        return render_template('recipe/create.html', categories=categories, form_data=request.form)

    db_path = current_app.config['DATABASE']
    new_id = recipe.create(db_path, name, description, category, cooking_time, servings)
    flash('食譜建立成功！', 'success')
    return redirect(url_for('recipe.detail', id=new_id))


@recipe_bp.route('/recipes/<int:id>')
def detail(id):
    """
    食譜詳情頁。
    """
    db_path = current_app.config['DATABASE']
    r = recipe.get_by_id(db_path, id)
    if not r:
        abort(404)
        
    ingredients = ingredient.get_by_recipe_id(db_path, id)
    steps = step.get_by_recipe_id(db_path, id)
    
    return render_template('recipe/detail.html', recipe=r, ingredients=ingredients, steps=steps)


@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_form(id):
    """
    編輯食譜表單頁面。
    """
    db_path = current_app.config['DATABASE']
    r = recipe.get_by_id(db_path, id)
    if not r:
        abort(404)
        
    categories = recipe.get_categories()
    return render_template('recipe/edit.html', recipe=r, categories=categories)


@recipe_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update(id):
    """
    更新食譜。
    """
    db_path = current_app.config['DATABASE']
    r = recipe.get_by_id(db_path, id)
    if not r:
        abort(404)
        
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', '其他')
    cooking_time = request.form.get('cooking_time')
    servings = request.form.get('servings')

    if not name:
        flash('食譜名稱為必填', 'error')
        categories = recipe.get_categories()
        return render_template('recipe/edit.html', recipe=r, categories=categories, form_data=request.form)

    recipe.update(db_path, id, name, description, category, cooking_time, servings)
    flash('食譜更新成功！', 'success')
    return redirect(url_for('recipe.detail', id=id))


@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除食譜。
    """
    db_path = current_app.config['DATABASE']
    r = recipe.get_by_id(db_path, id)
    if not r:
        abort(404)
        
    recipe.delete(db_path, id)
    flash('食譜已刪除', 'success')
    return redirect(url_for('recipe.index'))
