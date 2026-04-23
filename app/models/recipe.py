"""
Recipe Model — 食譜資料模型

提供食譜資料表的 CRUD 操作方法。
"""

import sqlite3
from datetime import datetime


def get_db_connection(db_path):
    """取得資料庫連線，啟用外鍵支援與 Row 物件。"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create(db_path, name, description='', category='其他', cooking_time=None, servings=None):
    """
    新增一道食譜。

    Args:
        db_path: 資料庫檔案路徑
        name: 食譜名稱（必填）
        description: 食譜描述
        category: 食譜分類
        cooking_time: 烹飪時間（分鐘）
        servings: 份量（幾人份）

    Returns:
        新建立的食譜 ID
    """
    conn = get_db_connection(db_path)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor = conn.execute(
            """INSERT INTO recipes (name, description, category, cooking_time, servings, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (name, description, category, cooking_time, servings, now, now)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_all(db_path, category=None):
    """
    取得所有食譜，可依分類篩選。

    Args:
        db_path: 資料庫檔案路徑
        category: 篩選分類（None 表示全部）

    Returns:
        食譜列表（sqlite3.Row 物件）
    """
    conn = get_db_connection(db_path)
    try:
        if category:
            rows = conn.execute(
                "SELECT * FROM recipes WHERE category = ? ORDER BY created_at DESC",
                (category,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM recipes ORDER BY created_at DESC"
            ).fetchall()
        return rows
    finally:
        conn.close()


def get_by_id(db_path, recipe_id):
    """
    依 ID 取得單一食譜。

    Args:
        db_path: 資料庫檔案路徑
        recipe_id: 食譜 ID

    Returns:
        食譜資料（sqlite3.Row 物件），找不到回傳 None
    """
    conn = get_db_connection(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM recipes WHERE id = ?",
            (recipe_id,)
        ).fetchone()
        return row
    finally:
        conn.close()


def update(db_path, recipe_id, name, description='', category='其他', cooking_time=None, servings=None):
    """
    更新食譜資訊。

    Args:
        db_path: 資料庫檔案路徑
        recipe_id: 食譜 ID
        name: 食譜名稱
        description: 食譜描述
        category: 食譜分類
        cooking_time: 烹飪時間（分鐘）
        servings: 份量（幾人份）

    Returns:
        受影響的資料列數
    """
    conn = get_db_connection(db_path)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor = conn.execute(
            """UPDATE recipes
               SET name = ?, description = ?, category = ?,
                   cooking_time = ?, servings = ?, updated_at = ?
               WHERE id = ?""",
            (name, description, category, cooking_time, servings, now, recipe_id)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def delete(db_path, recipe_id):
    """
    刪除食譜（連帶刪除相關材料與步驟，由外鍵 CASCADE 處理）。

    Args:
        db_path: 資料庫檔案路徑
        recipe_id: 食譜 ID

    Returns:
        受影響的資料列數
    """
    conn = get_db_connection(db_path)
    try:
        cursor = conn.execute(
            "DELETE FROM recipes WHERE id = ?",
            (recipe_id,)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def search(db_path, keyword):
    """
    依關鍵字搜尋食譜（搜尋食譜名稱與材料名稱）。

    Args:
        db_path: 資料庫檔案路徑
        keyword: 搜尋關鍵字

    Returns:
        符合條件的食譜列表（去重複）
    """
    conn = get_db_connection(db_path)
    try:
        like_pattern = f'%{keyword}%'

        # 搜尋食譜名稱
        rows = conn.execute(
            """SELECT DISTINCT r.* FROM recipes r
               WHERE r.name LIKE ?
               UNION
               SELECT DISTINCT r.* FROM recipes r
               JOIN ingredients i ON r.id = i.recipe_id
               WHERE i.name LIKE ?
               ORDER BY created_at DESC""",
            (like_pattern, like_pattern)
        ).fetchall()
        return rows
    finally:
        conn.close()


def get_categories():
    """
    取得所有預設分類。

    Returns:
        分類名稱列表
    """
    return ['中式', '西式', '日式', '韓式', '東南亞', '甜點', '飲品', '其他']
