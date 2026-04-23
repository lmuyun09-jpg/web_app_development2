-- ============================================
-- 食譜收藏夾 — SQLite 資料庫建表語法
-- ============================================

-- 啟用外鍵支援（SQLite 預設關閉）
PRAGMA foreign_keys = ON;

-- ============================================
-- 食譜資料表
-- ============================================
CREATE TABLE IF NOT EXISTS recipes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    description   TEXT    DEFAULT '',
    category      TEXT    NOT NULL DEFAULT '其他',
    cooking_time  INTEGER DEFAULT NULL,
    servings      INTEGER DEFAULT NULL,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at    TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ============================================
-- 材料資料表
-- ============================================
CREATE TABLE IF NOT EXISTS ingredients (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id   INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    amount      TEXT    DEFAULT '',
    unit        TEXT    DEFAULT '',
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- ============================================
-- 步驟資料表
-- ============================================
CREATE TABLE IF NOT EXISTS steps (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id     INTEGER NOT NULL,
    step_number   INTEGER NOT NULL,
    description   TEXT    NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- ============================================
-- 索引（提升查詢效能）
-- ============================================
CREATE INDEX IF NOT EXISTS idx_ingredients_recipe_id ON ingredients(recipe_id);
CREATE INDEX IF NOT EXISTS idx_steps_recipe_id ON steps(recipe_id);
CREATE INDEX IF NOT EXISTS idx_recipes_category ON recipes(category);
