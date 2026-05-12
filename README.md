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

## 快速建立日報

- 執行：`python3 scripts/new_report.py --agent frontend-dashboard-agent`
- 指定日期：`python3 scripts/new_report.py --agent frontend-dashboard-agent --date 2026-05-13`
- 覆蓋既有檔案：`python3 scripts/new_report.py --agent frontend-dashboard-agent --date 2026-05-13 --force`

## 本機預覽

- 執行：`python3 -m http.server 8081`
- 開啟：`http://localhost:8081`

## Vercel 部署

- 這個 repo 現在可直接作為靜態網站部署到 Vercel
- Vercel 會讀取根目錄的 `index.html`
- `vercel.json` 已補上基本設定

## 自動更新流程

- GitHub Actions workflow：`.github/workflows/refresh-dashboard.yml`
- 當 `reports/`、dashboard schema 或生成腳本更新時，會自動重建 `dashboard/data/latest.json`
- 也會在每天台北時間 00:00 嘗試重建一次資料
- 如果首次自動回寫失敗，請檢查 repository 的 Actions workflow 權限是否允許寫入內容

## 每日操作說明

- 詳細流程請看：`docs/daily-ops.md`

## 下一步

- 開始把各代理的日報依路徑規則放入 `reports/`
- 依模板產生每日總覽 JSON，寫入 `dashboard/data/`
- 再由 `localhost:8081` 讀取 `dashboard/data/` 顯示
