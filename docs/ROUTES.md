# 食譜收藏夾 — 路由設計文件

## 1. 路由總覽表格

### 食譜相關路由

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 首頁 / 食譜列表 | GET | `/` 或 `/recipes` | `templates/index.html` | 顯示所有食譜，支援分類篩選 |
| 新增食譜頁面 | GET | `/recipes/create` | `templates/recipe/create.html` | 顯示新增食譜表單 |
| 建立食譜 | POST | `/recipes/create` | — | 接收表單，存入 DB，重導向到詳情頁 |
| 食譜詳情 | GET | `/recipes/<id>` | `templates/recipe/detail.html` | 顯示食譜完整資訊（含材料與步驟） |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `templates/recipe/edit.html` | 顯示編輯食譜表單 |
| 更新食譜 | POST | `/recipes/<id>/edit` | — | 接收修改資料，更新 DB，重導向到詳情頁 |
| 刪除食譜 | POST | `/recipes/<id>/delete` | — | 刪除食譜及相關資料，重導向到列表頁 |

### 材料相關路由

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 新增材料 | POST | `/recipes/<id>/ingredients` | — | 新增材料，重導向到食譜詳情頁 |
| 編輯材料 | POST | `/recipes/<id>/ingredients/<ing_id>/edit` | — | 更新材料，重導向到食譜詳情頁 |
| 刪除材料 | POST | `/recipes/<id>/ingredients/<ing_id>/delete` | — | 刪除材料，重導向到食譜詳情頁 |

### 步驟相關路由

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 新增步驟 | POST | `/recipes/<id>/steps` | — | 新增步驟（自動編號），重導向到食譜詳情頁 |
| 編輯步驟 | POST | `/recipes/<id>/steps/<step_id>/edit` | — | 更新步驟內容，重導向到食譜詳情頁 |
| 刪除步驟 | POST | `/recipes/<id>/steps/<step_id>/delete` | — | 刪除步驟並重新編號，重導向到食譜詳情頁 |
| 步驟上移 | POST | `/recipes/<id>/steps/<step_id>/move-up` | — | 步驟順序上移，重導向到食譜詳情頁 |
| 步驟下移 | POST | `/recipes/<id>/steps/<step_id>/move-down` | — | 步驟順序下移，重導向到食譜詳情頁 |

### 搜尋相關路由

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 搜尋食譜 | GET | `/search` | `templates/search/results.html` | 依關鍵字搜尋食譜名稱與材料 |

---

## 2. 每個路由的詳細說明

### 2-1. 食譜路由

#### `GET /` 或 `GET /recipes` — 食譜列表

- **輸入：** Query 參數 `category`（選填，用於篩選分類）
- **處理邏輯：**
  1. 若有 `category` 參數，呼叫 `recipe.get_all(db_path, category=category)`
  2. 若無，呼叫 `recipe.get_all(db_path)`
  3. 呼叫 `recipe.get_categories()` 取得分類清單供篩選
- **輸出：** 渲染 `index.html`，傳入 `recipes` 列表與 `categories` 清單
- **錯誤處理：** 無特殊錯誤情況

#### `GET /recipes/create` — 新增食譜頁面

- **輸入：** 無
- **處理邏輯：** 呼叫 `recipe.get_categories()` 取得分類清單
- **輸出：** 渲染 `recipe/create.html`，傳入 `categories` 清單
- **錯誤處理：** 無

#### `POST /recipes/create` — 建立食譜

- **輸入：** 表單欄位 `name`（必填）、`description`、`category`、`cooking_time`、`servings`
- **處理邏輯：**
  1. 驗證 `name` 不為空
  2. 呼叫 `recipe.create(db_path, name, description, category, cooking_time, servings)`
  3. 取得新食譜 ID
- **輸出：** 重導向到 `/recipes/<new_id>`
- **錯誤處理：** `name` 為空時，重新渲染表單並顯示錯誤訊息

#### `GET /recipes/<id>` — 食譜詳情

- **輸入：** URL 參數 `id`（食譜 ID）
- **處理邏輯：**
  1. 呼叫 `recipe.get_by_id(db_path, id)` 取得食譜
  2. 呼叫 `ingredient.get_by_recipe_id(db_path, id)` 取得材料清單
  3. 呼叫 `step.get_by_recipe_id(db_path, id)` 取得步驟清單
- **輸出：** 渲染 `recipe/detail.html`，傳入 `recipe`、`ingredients`、`steps`
- **錯誤處理：** 找不到食譜時回傳 404

#### `GET /recipes/<id>/edit` — 編輯食譜頁面

- **輸入：** URL 參數 `id`
- **處理邏輯：**
  1. 呼叫 `recipe.get_by_id(db_path, id)` 取得食譜
  2. 呼叫 `recipe.get_categories()` 取得分類清單
- **輸出：** 渲染 `recipe/edit.html`，傳入 `recipe` 與 `categories`
- **錯誤處理：** 找不到食譜時回傳 404

#### `POST /recipes/<id>/edit` — 更新食譜

- **輸入：** URL 參數 `id`；表單欄位 `name`（必填）、`description`、`category`、`cooking_time`、`servings`
- **處理邏輯：**
  1. 驗證 `name` 不為空
  2. 呼叫 `recipe.update(db_path, id, name, description, category, cooking_time, servings)`
- **輸出：** 重導向到 `/recipes/<id>`
- **錯誤處理：** `name` 為空時重新渲染表單；找不到食譜時回傳 404

#### `POST /recipes/<id>/delete` — 刪除食譜

- **輸入：** URL 參數 `id`
- **處理邏輯：** 呼叫 `recipe.delete(db_path, id)`（CASCADE 自動刪除材料與步驟）
- **輸出：** 重導向到 `/recipes`
- **錯誤處理：** 找不到食譜時回傳 404

---

### 2-2. 材料路由

#### `POST /recipes/<id>/ingredients` — 新增材料

- **輸入：** URL 參數 `id`；表單欄位 `name`（必填）、`amount`、`unit`
- **處理邏輯：**
  1. 驗證 `name` 不為空
  2. 呼叫 `ingredient.create(db_path, id, name, amount, unit)`
- **輸出：** 重導向到 `/recipes/<id>`
- **錯誤處理：** `name` 為空時重導向並顯示錯誤

#### `POST /recipes/<id>/ingredients/<ing_id>/edit` — 編輯材料

- **輸入：** URL 參數 `id`、`ing_id`；表單欄位 `name`（必填）、`amount`、`unit`
- **處理邏輯：**
  1. 驗證 `name` 不為空
  2. 呼叫 `ingredient.update(db_path, ing_id, name, amount, unit)`
- **輸出：** 重導向到 `/recipes/<id>`
- **錯誤處理：** 找不到材料時回傳 404

#### `POST /recipes/<id>/ingredients/<ing_id>/delete` — 刪除材料

- **輸入：** URL 參數 `id`、`ing_id`
- **處理邏輯：** 呼叫 `ingredient.delete(db_path, ing_id)`
- **輸出：** 重導向到 `/recipes/<id>`
- **錯誤處理：** 找不到材料時回傳 404

---

### 2-3. 步驟路由

#### `POST /recipes/<id>/steps` — 新增步驟

- **輸入：** URL 參數 `id`；表單欄位 `description`（必填）
- **處理邏輯：**
  1. 驗證 `description` 不為空
  2. 呼叫 `step.create(db_path, id, description)`（自動編號）
- **輸出：** 重導向到 `/recipes/<id>`
- **錯誤處理：** `description` 為空時重導向並顯示錯誤

#### `POST /recipes/<id>/steps/<step_id>/edit` — 編輯步驟

- **輸入：** URL 參數 `id`、`step_id`；表單欄位 `description`（必填）
- **處理邏輯：** 呼叫 `step.update(db_path, step_id, description)`
- **輸出：** 重導向到 `/recipes/<id>`
- **錯誤處理：** 找不到步驟時回傳 404

#### `POST /recipes/<id>/steps/<step_id>/delete` — 刪除步驟

- **輸入：** URL 參數 `id`、`step_id`
- **處理邏輯：** 呼叫 `step.delete(db_path, step_id)`（自動重新編號）
- **輸出：** 重導向到 `/recipes/<id>`
- **錯誤處理：** 找不到步驟時回傳 404

#### `POST /recipes/<id>/steps/<step_id>/move-up` — 步驟上移

- **輸入：** URL 參數 `id`、`step_id`
- **處理邏輯：** 呼叫 `step.move_up(db_path, step_id)`
- **輸出：** 重導向到 `/recipes/<id>`
- **錯誤處理：** 已在最上方則不動作

#### `POST /recipes/<id>/steps/<step_id>/move-down` — 步驟下移

- **輸入：** URL 參數 `id`、`step_id`
- **處理邏輯：** 呼叫 `step.move_down(db_path, step_id)`
- **輸出：** 重導向到 `/recipes/<id>`
- **錯誤處理：** 已在最下方則不動作

---

### 2-4. 搜尋路由

#### `GET /search` — 搜尋食譜

- **輸入：** Query 參數 `q`（搜尋關鍵字）
- **處理邏輯：**
  1. 取得關鍵字 `q`
  2. 若 `q` 不為空，呼叫 `recipe.search(db_path, q)`
  3. 若 `q` 為空，回傳空結果
- **輸出：** 渲染 `search/results.html`，傳入 `recipes` 結果與 `keyword`
- **錯誤處理：** 無特殊錯誤情況

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承自 | 用途 |
|----------|--------|------|
| `templates/base.html` | — | 基礎版型（header、footer、導覽列、CSS/JS 引入） |
| `templates/index.html` | `base.html` | 首頁 / 食譜列表頁（含分類篩選） |
| `templates/recipe/create.html` | `base.html` | 新增食譜表單 |
| `templates/recipe/detail.html` | `base.html` | 食譜詳情頁（含材料清單、步驟清單、新增表單） |
| `templates/recipe/edit.html` | `base.html` | 編輯食譜表單 |
| `templates/search/results.html` | `base.html` | 搜尋結果頁 |

### 模板繼承架構

```
base.html
├── index.html
├── recipe/
│   ├── create.html
│   ├── detail.html
│   └── edit.html
└── search/
    └── results.html
```

---

## 4. 路由骨架程式碼

路由骨架檔案位於 `app/routes/`，每個檔案只包含函式定義與 docstring：

| 檔案 | Blueprint 名稱 | 負責功能 |
|------|----------------|---------|
| `app/routes/__init__.py` | — | 套件初始化 |
| `app/routes/recipe.py` | `recipe_bp` | 食譜 CRUD（7 個路由） |
| `app/routes/ingredient.py` | `ingredient_bp` | 材料管理（3 個路由） |
| `app/routes/step.py` | `step_bp` | 步驟管理（5 個路由） |
| `app/routes/search.py` | `search_bp` | 搜尋功能（1 個路由） |

---

*文件建立日期：2026-04-23*
*最後更新日期：2026-04-23*
