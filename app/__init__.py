"""
App 套件初始化 — Flask 應用程式工廠

建立並設定 Flask app 實例，註冊所有 Blueprint，
提供資料庫初始化函式。
"""

import os
import sqlite3
from flask import Flask
from config import Config


def create_app():
    """
    建立 Flask app 實例（Application Factory 模式）。

    Returns:
        Flask app 實例
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # 確保 instance 資料夾存在
    instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
    os.makedirs(instance_path, exist_ok=True)

    # 註冊 Blueprint
    from app.routes.recipe import recipe_bp
    from app.routes.ingredient import ingredient_bp
    from app.routes.step import step_bp
    from app.routes.search import search_bp

    app.register_blueprint(recipe_bp)
    app.register_blueprint(ingredient_bp)
    app.register_blueprint(step_bp)
    app.register_blueprint(search_bp)

    return app


def init_db():
    """
    初始化資料庫：讀取 schema.sql 並執行建表語句。

    使用方式：
        python -c "from app import init_db; init_db()"
    """
    from config import Config

    # 確保 instance 資料夾存在
    db_dir = os.path.dirname(Config.DATABASE)
    os.makedirs(db_dir, exist_ok=True)

    # 讀取 schema.sql
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    # 執行建表語句
    conn = sqlite3.connect(Config.DATABASE)
    try:
        conn.executescript(schema_sql)
        conn.commit()
        print(f"資料庫初始化成功：{Config.DATABASE}")
    finally:
        conn.close()
