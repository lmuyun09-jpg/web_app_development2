"""
Ingredient Model — 材料資料模型

提供材料資料表的 CRUD 操作方法。
"""

import sqlite3


def get_db_connection(db_path):
    """取得資料庫連線，啟用外鍵支援與 Row 物件。"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create(db_path, recipe_id, name, amount='', unit=''):
    """
    新增一項材料。

    Args:
        db_path: 資料庫檔案路徑
        recipe_id: 所屬食譜 ID
        name: 材料名稱（必填）
        amount: 數量
        unit: 單位

    Returns:
        新建立的材料 ID
    """
    conn = get_db_connection(db_path)
    try:
        cursor = conn.execute(
            """INSERT INTO ingredients (recipe_id, name, amount, unit)
               VALUES (?, ?, ?, ?)""",
            (recipe_id, name, amount, unit)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_by_recipe_id(db_path, recipe_id):
    """
    取得某道食譜的所有材料。

    Args:
        db_path: 資料庫檔案路徑
        recipe_id: 食譜 ID

    Returns:
        材料列表（sqlite3.Row 物件）
    """
    conn = get_db_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT * FROM ingredients WHERE recipe_id = ? ORDER BY id",
            (recipe_id,)
        ).fetchall()
        return rows
    finally:
        conn.close()


def get_by_id(db_path, ingredient_id):
    """
    依 ID 取得單一材料。

    Args:
        db_path: 資料庫檔案路徑
        ingredient_id: 材料 ID

    Returns:
        材料資料（sqlite3.Row 物件），找不到回傳 None
    """
    conn = get_db_connection(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM ingredients WHERE id = ?",
            (ingredient_id,)
        ).fetchone()
        return row
    finally:
        conn.close()


def update(db_path, ingredient_id, name, amount='', unit=''):
    """
    更新材料資訊。

    Args:
        db_path: 資料庫檔案路徑
        ingredient_id: 材料 ID
        name: 材料名稱
        amount: 數量
        unit: 單位

    Returns:
        受影響的資料列數
    """
    conn = get_db_connection(db_path)
    try:
        cursor = conn.execute(
            """UPDATE ingredients
               SET name = ?, amount = ?, unit = ?
               WHERE id = ?""",
            (name, amount, unit, ingredient_id)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def delete(db_path, ingredient_id):
    """
    刪除一項材料。

    Args:
        db_path: 資料庫檔案路徑
        ingredient_id: 材料 ID

    Returns:
        受影響的資料列數
    """
    conn = get_db_connection(db_path)
    try:
        cursor = conn.execute(
            "DELETE FROM ingredients WHERE id = ?",
            (ingredient_id,)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()
