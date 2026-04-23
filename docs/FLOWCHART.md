# 食譜收藏夾 — 流程圖文件

## 1. 使用者流程圖（User Flow）

以下流程圖展示使用者從進入網站開始，可以執行的所有主要操作路徑。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 食譜列表]

    B --> C{要執行什麼操作？}

    C -->|新增食譜| D[填寫食譜表單]
    D --> D1[輸入名稱/描述/分類/時間/份量]
    D1 --> D2[送出表單]
    D2 --> E[食譜詳情頁]
    E --> E1[新增材料]
    E1 --> E1a[輸入材料名稱/數量/單位]
    E1a --> E
    E --> E2[新增步驟]
    E2 --> E2a[輸入步驟內容]
    E2a --> E

    C -->|查看食譜| F[點選食譜]
    F --> E

    C -->|編輯食譜| G[點選編輯按鈕]
    G --> G1[修改食譜資訊]
    G1 --> G2[送出修改]
    G2 --> E

    C -->|刪除食譜| H[點選刪除按鈕]
    H --> H1{確認刪除？}
    H1 -->|是| H2[刪除食譜及相關資料]
    H2 --> B
    H1 -->|否| B

    C -->|搜尋食譜| I[輸入搜尋關鍵字]
    I --> I1[搜尋結果頁]
    I1 --> F

    C -->|篩選分類| J[選擇食譜分類]
    J --> J1[顯示該分類食譜]
    J1 --> F
```

### 流程說明

1. **進入首頁**：使用者開啟網站後，看到所有食譜的列表
2. **新增食譜**：填寫表單建立食譜 → 進入詳情頁 → 可繼續新增材料與步驟
3. **查看食譜**：從列表點選任一食譜，進入詳情頁查看完整資訊
4. **編輯食譜**：在詳情頁點選編輯，修改後儲存回到詳情頁
5. **刪除食譜**：點選刪除按鈕，確認後刪除並返回列表
6. **搜尋食譜**：輸入關鍵字搜尋，從搜尋結果進入食譜詳情
7. **篩選分類**：選擇分類篩選食譜列表

---

## 2. 系統序列圖（Sequence Diagram）

### 2-1. 新增食譜流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 點擊「新增食譜」
    Browser->>Flask: GET /recipes/create
    Flask-->>Browser: 回傳 create.html 表單頁面

    User->>Browser: 填寫食譜資訊並送出
    Browser->>Flask: POST /recipes/create
    Flask->>Model: create_recipe(name, desc, category, time, servings)
    Model->>DB: INSERT INTO recipes VALUES(...)
    DB-->>Model: 回傳新食譜 ID
    Model-->>Flask: 回傳 recipe_id
    Flask-->>Browser: 重導向到 /recipes/{id}
```

### 2-2. 新增材料流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Ingredient Model
    participant DB as SQLite

    User->>Browser: 在食譜詳情頁填寫材料資訊
    Browser->>Flask: POST /recipes/{id}/ingredients
    Flask->>Model: create_ingredient(recipe_id, name, amount, unit)
    Model->>DB: INSERT INTO ingredients VALUES(...)
    DB-->>Model: 成功
    Model-->>Flask: 回傳結果
    Flask-->>Browser: 重導向到 /recipes/{id}
    Browser-->>User: 顯示更新後的食譜詳情（含新材料）
```

### 2-3. 新增步驟流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Step Model
    participant DB as SQLite

    User->>Browser: 在食譜詳情頁填寫步驟內容
    Browser->>Flask: POST /recipes/{id}/steps
    Flask->>Model: create_step(recipe_id, description)
    Model->>DB: SELECT MAX(step_number) FROM steps WHERE recipe_id=...
    DB-->>Model: 目前最大步驟編號
    Model->>DB: INSERT INTO steps VALUES(...)
    DB-->>Model: 成功
    Model-->>Flask: 回傳結果
    Flask-->>Browser: 重導向到 /recipes/{id}
    Browser-->>User: 顯示更新後的食譜詳情（含新步驟）
```

### 2-4. 搜尋食譜流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Recipe/Ingredient Model
    participant DB as SQLite

    User->>Browser: 在搜尋欄輸入關鍵字
    Browser->>Flask: GET /search?q=關鍵字
    Flask->>Model: search_recipes(keyword)
    Model->>DB: SELECT * FROM recipes WHERE name LIKE '%關鍵字%'
    DB-->>Model: 符合名稱的食譜
    Model->>DB: SELECT DISTINCT recipe_id FROM ingredients WHERE name LIKE '%關鍵字%'
    DB-->>Model: 符合材料的食譜 ID
    Model-->>Flask: 合併搜尋結果
    Flask-->>Browser: 渲染 results.html
    Browser-->>User: 顯示搜尋結果列表
```

### 2-5. 刪除食譜流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 點擊「刪除」按鈕
    Browser-->>User: 顯示確認對話框
    User->>Browser: 確認刪除

    Browser->>Flask: POST /recipes/{id}/delete
    Flask->>Model: delete_recipe(id)
    Model->>DB: DELETE FROM steps WHERE recipe_id=...
    DB-->>Model: 成功
    Model->>DB: DELETE FROM ingredients WHERE recipe_id=...
    DB-->>Model: 成功
    Model->>DB: DELETE FROM recipes WHERE id=...
    DB-->>Model: 成功
    Model-->>Flask: 刪除完成
    Flask-->>Browser: 重導向到 /recipes
    Browser-->>User: 顯示更新後的食譜列表
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|----------|-----------|------|
| 首頁 / 食譜列表 | `/` 或 `/recipes` | GET | 顯示所有食譜列表，支援分類篩選 |
| 新增食譜表單 | `/recipes/create` | GET | 顯示新增食譜的表單頁面 |
| 新增食譜 | `/recipes/create` | POST | 接收表單資料，建立新食譜 |
| 食譜詳情 | `/recipes/<id>` | GET | 顯示食譜完整資訊（含材料與步驟） |
| 編輯食譜表單 | `/recipes/<id>/edit` | GET | 顯示編輯食譜的表單頁面 |
| 更新食譜 | `/recipes/<id>/edit` | POST | 接收修改資料，更新食譜 |
| 刪除食譜 | `/recipes/<id>/delete` | POST | 刪除食譜及其所有材料與步驟 |
| 新增材料 | `/recipes/<id>/ingredients` | POST | 為食譜新增一項材料 |
| 編輯材料 | `/recipes/<id>/ingredients/<ing_id>/edit` | POST | 更新材料資訊 |
| 刪除材料 | `/recipes/<id>/ingredients/<ing_id>/delete` | POST | 刪除一項材料 |
| 新增步驟 | `/recipes/<id>/steps` | POST | 為食譜新增一個步驟 |
| 編輯步驟 | `/recipes/<id>/steps/<step_id>/edit` | POST | 更新步驟內容 |
| 刪除步驟 | `/recipes/<id>/steps/<step_id>/delete` | POST | 刪除一個步驟並重新編號 |
| 步驟上移 | `/recipes/<id>/steps/<step_id>/move-up` | POST | 將步驟順序上移一位 |
| 步驟下移 | `/recipes/<id>/steps/<step_id>/move-down` | POST | 將步驟順序下移一位 |
| 搜尋食譜 | `/search` | GET | 依關鍵字搜尋食譜名稱與材料 |

---

*文件建立日期：2026-04-23*
*最後更新日期：2026-04-23*
