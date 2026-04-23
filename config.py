"""
Config — 應用程式設定

集中管理 Flask 設定值，包含資料庫路徑、密鑰等。
"""

import os

# 取得專案根目錄的絕對路徑
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Flask 應用程式設定。"""

    # Flask 密鑰（用於 session 與 CSRF 保護）
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change-in-production')

    # SQLite 資料庫路徑
    DATABASE = os.path.join(BASE_DIR, 'instance', 'database.db')

    # 偵錯模式
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
