# 代理總覽儀表板

這個 repository 用來整理每日代理報告、結合行事曆脈絡，並準備可供本機儀表板使用的總覽內容。

## Repository 結構

- `AGENTS.md`: 工作規則與代理行為說明
- `reports/`: 各代理每日 Markdown 報告
- `dashboard/`: 儀表板輸出 schema、範例與發布用資料目錄
- `docs/`: 路徑規則、欄位定義與維護說明
- `scripts/`: 產生每日 dashboard 輸出的腳本

## 每日報告路徑規則

- 建議固定使用 `reports/{agent_name}/YYYY-MM-DD.md`
- 範例：`reports/research-agent/2026-05-12.md`
- 模板可直接從 `reports/_template/AGENT_NAME/YYYY-MM-DD.md` 複製

## Dashboard 輸出

- 固定骨架與欄位定義：`dashboard/schema/dashboard-schema.json`
- 每日輸出範例：`dashboard/examples/daily-dashboard.example.json`
- 可發布資料目錄：`dashboard/data/`

## 前端介面

- 入口頁面：`index.html`
- 樣式：`styles.css`
- 前端邏輯：`app.js`
- 預設讀取：`dashboard/data/latest.json`

## 產生每日總覽

- 執行：`python3 scripts/build_dashboard.py`
- 指定日期：`python3 scripts/build_dashboard.py --date 2026-05-12`
- 預設會讀取 `reports/`，並輸出到 `dashboard/data/YYYY-MM-DD.json` 與 `dashboard/data/latest.json`

## 本機預覽

- 執行：`python3 -m http.server 8081`
- 開啟：`http://localhost:8081`

## Vercel 部署

- 這個 repo 現在可直接作為靜態網站部署到 Vercel
- Vercel 會讀取根目錄的 `index.html`
- `vercel.json` 已補上基本設定

## 下一步

- 開始把各代理的日報依路徑規則放入 `reports/`
- 依模板產生每日總覽 JSON，寫入 `dashboard/data/`
- 再由 `localhost:8081` 讀取 `dashboard/data/` 顯示
