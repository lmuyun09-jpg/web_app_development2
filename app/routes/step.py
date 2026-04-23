"""
Step Routes — 步驟路由

處理步驟的新增、編輯、刪除與排序操作。
所有操作完成後重導向到食譜詳情頁。
"""

from flask import Blueprint, request, redirect, url_for, abort

step_bp = Blueprint('step', __name__)


@step_bp.route('/recipes/<int:id>/steps', methods=['POST'])
def create(id):
    """
    新增步驟。

    - POST /recipes/<id>/steps

    接收表單資料（description），
    驗證 description 不為空，呼叫 step.create()（自動編號），
    重導向到 /recipes/<id>。
    """
    pass


@step_bp.route('/recipes/<int:id>/steps/<int:step_id>/edit', methods=['POST'])
def update(id, step_id):
    """
    編輯步驟。

    - POST /recipes/<id>/steps/<step_id>/edit

    接收表單資料（description），
    驗證 description 不為空，呼叫 step.update()，
    重導向到 /recipes/<id>。
    找不到步驟時回傳 404。
    """
    pass


@step_bp.route('/recipes/<int:id>/steps/<int:step_id>/delete', methods=['POST'])
def delete(id, step_id):
    """
    刪除步驟。

    - POST /recipes/<id>/steps/<step_id>/delete

    呼叫 step.delete()（自動重新編號），
    重導向到 /recipes/<id>。
    找不到步驟時回傳 404。
    """
    pass


@step_bp.route('/recipes/<int:id>/steps/<int:step_id>/move-up', methods=['POST'])
def move_up(id, step_id):
    """
    步驟上移。

    - POST /recipes/<id>/steps/<step_id>/move-up

    呼叫 step.move_up()，與前一個步驟交換順序，
    重導向到 /recipes/<id>。
    已在最上方則不動作。
    """
    pass


@step_bp.route('/recipes/<int:id>/steps/<int:step_id>/move-down', methods=['POST'])
def move_down(id, step_id):
    """
    步驟下移。

    - POST /recipes/<id>/steps/<step_id>/move-down

    呼叫 step.move_down()，與後一個步驟交換順序，
    重導向到 /recipes/<id>。
    已在最下方則不動作。
    """
    pass
