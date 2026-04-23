"""
Step Model — 步驟資料模型

提供步驟資料表的 CRUD 操作方法，包含步驟排序功能。
"""

import sqlite3


def get_db_connection(db_path):
    """取得資料庫連線，啟用外鍵支援與 Row 物件。"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create(db_path, recipe_id, description):
    """
    新增一個步驟（自動編號，排在最後）。

    Args:
        db_path: 資料庫檔案路徑
        recipe_id: 所屬食譜 ID
        description: 步驟內容（必填）

    Returns:
        新建立的步驟 ID
    """
    conn = get_db_connection(db_path)
    try:
        # 取得目前最大步驟編號
        row = conn.execute(
            "SELECT COALESCE(MAX(step_number), 0) as max_num FROM steps WHERE recipe_id = ?",
            (recipe_id,)
        ).fetchone()
        next_number = row['max_num'] + 1

        cursor = conn.execute(
            """INSERT INTO steps (recipe_id, step_number, description)
               VALUES (?, ?, ?)""",
            (recipe_id, next_number, description)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_by_recipe_id(db_path, recipe_id):
    """
    取得某道食譜的所有步驟（依步驟編號排序）。

    Args:
        db_path: 資料庫檔案路徑
        recipe_id: 食譜 ID

    Returns:
        步驟列表（sqlite3.Row 物件）
    """
    conn = get_db_connection(db_path)
    try:
        rows = conn.execute(
            "SELECT * FROM steps WHERE recipe_id = ? ORDER BY step_number",
            (recipe_id,)
        ).fetchall()
        return rows
    finally:
        conn.close()


def get_by_id(db_path, step_id):
    """
    依 ID 取得單一步驟。

    Args:
        db_path: 資料庫檔案路徑
        step_id: 步驟 ID

    Returns:
        步驟資料（sqlite3.Row 物件），找不到回傳 None
    """
    conn = get_db_connection(db_path)
    try:
        row = conn.execute(
            "SELECT * FROM steps WHERE id = ?",
            (step_id,)
        ).fetchone()
        return row
    finally:
        conn.close()


def update(db_path, step_id, description):
    """
    更新步驟內容。

    Args:
        db_path: 資料庫檔案路徑
        step_id: 步驟 ID
        description: 步驟內容

    Returns:
        受影響的資料列數
    """
    conn = get_db_connection(db_path)
    try:
        cursor = conn.execute(
            "UPDATE steps SET description = ? WHERE id = ?",
            (description, step_id)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def delete(db_path, step_id):
    """
    刪除一個步驟，並重新編號該食譜的所有步驟。

    Args:
        db_path: 資料庫檔案路徑
        step_id: 步驟 ID

    Returns:
        受影響的資料列數
    """
    conn = get_db_connection(db_path)
    try:
        # 先取得該步驟所屬的食譜 ID
        step = conn.execute(
            "SELECT recipe_id FROM steps WHERE id = ?",
            (step_id,)
        ).fetchone()

        if not step:
            return 0

        recipe_id = step['recipe_id']

        # 刪除步驟
        cursor = conn.execute(
            "DELETE FROM steps WHERE id = ?",
            (step_id,)
        )

        # 重新編號剩餘步驟
        _renumber_steps(conn, recipe_id)

        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def move_up(db_path, step_id):
    """
    將步驟上移一位（與前一個步驟交換順序）。

    Args:
        db_path: 資料庫檔案路徑
        step_id: 步驟 ID

    Returns:
        是否成功移動（True/False）
    """
    conn = get_db_connection(db_path)
    try:
        current = conn.execute(
            "SELECT * FROM steps WHERE id = ?",
            (step_id,)
        ).fetchone()

        if not current or current['step_number'] <= 1:
            return False

        # 找到前一個步驟
        previous = conn.execute(
            """SELECT * FROM steps
               WHERE recipe_id = ? AND step_number = ?""",
            (current['recipe_id'], current['step_number'] - 1)
        ).fetchone()

        if not previous:
            return False

        # 交換步驟編號
        conn.execute(
            "UPDATE steps SET step_number = ? WHERE id = ?",
            (current['step_number'], previous['id'])
        )
        conn.execute(
            "UPDATE steps SET step_number = ? WHERE id = ?",
            (previous['step_number'], current['id'])
        )
        conn.commit()
        return True
    finally:
        conn.close()


def move_down(db_path, step_id):
    """
    將步驟下移一位（與後一個步驟交換順序）。

    Args:
        db_path: 資料庫檔案路徑
        step_id: 步驟 ID

    Returns:
        是否成功移動（True/False）
    """
    conn = get_db_connection(db_path)
    try:
        current = conn.execute(
            "SELECT * FROM steps WHERE id = ?",
            (step_id,)
        ).fetchone()

        if not current:
            return False

        # 取得該食譜的最大步驟編號
        max_row = conn.execute(
            "SELECT MAX(step_number) as max_num FROM steps WHERE recipe_id = ?",
            (current['recipe_id'],)
        ).fetchone()

        if current['step_number'] >= max_row['max_num']:
            return False

        # 找到後一個步驟
        next_step = conn.execute(
            """SELECT * FROM steps
               WHERE recipe_id = ? AND step_number = ?""",
            (current['recipe_id'], current['step_number'] + 1)
        ).fetchone()

        if not next_step:
            return False

        # 交換步驟編號
        conn.execute(
            "UPDATE steps SET step_number = ? WHERE id = ?",
            (current['step_number'], next_step['id'])
        )
        conn.execute(
            "UPDATE steps SET step_number = ? WHERE id = ?",
            (next_step['step_number'], current['id'])
        )
        conn.commit()
        return True
    finally:
        conn.close()


def _renumber_steps(conn, recipe_id):
    """
    重新編號某道食譜的所有步驟（內部方法）。

    Args:
        conn: 資料庫連線（由呼叫端管理）
        recipe_id: 食譜 ID
    """
    steps = conn.execute(
        "SELECT id FROM steps WHERE recipe_id = ? ORDER BY step_number",
        (recipe_id,)
    ).fetchall()

    for index, step in enumerate(steps, start=1):
        conn.execute(
            "UPDATE steps SET step_number = ? WHERE id = ?",
            (index, step['id'])
        )
