"""
app.py — 應用程式入口點

啟動 Flask 開發伺服器。

使用方式：
    python app.py
    或
    flask run
"""

from app import create_app, init_db

app = create_app()

# 首次啟動時自動初始化資料庫
init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
