# Daily Ops

## 你每天的固定流程

1. 為今天需要更新的代理建立日報
2. 填入每個代理的今日重點、風險、待跟進與摘要
3. 重建 dashboard data
4. 打開首頁確認摘要與排序
5. push 到 GitHub，讓 Vercel 與 GitHub Actions 接手刷新

## 建立新日報

### 方式一：快速建立器

- `python3 scripts/new_report.py --agent frontend-dashboard-agent`
- 指定日期：`python3 scripts/new_report.py --agent frontend-dashboard-agent --date 2026-05-13`
- 若要覆蓋既有檔案：`python3 scripts/new_report.py --agent frontend-dashboard-agent --date 2026-05-13 --force`

### 方式二：手動建立

- 路徑格式：`reports/{agent_name}/YYYY-MM-DD.md`
- 可從 `reports/_template/AGENT_NAME/YYYY-MM-DD.md` 複製

## 更新完日報後

- 重建資料：`python3 scripts/build_dashboard.py`
- 本機預覽：`python3 -m http.server 8081`
- 打開：`http://localhost:8081`

## 你每天最值得看的地方

### 第一層：先看 dashboard 首頁

- 頂部摘要：今天整體狀況
- 關鍵指標：阻塞數、待跟進數、需決策數
- 今日優先事項：今天最該先看的 3 到 5 件事
- 風險與提醒：需要人工介入的項目

### 第二層：再看個別代理日報

- 先看 `latest_status`
- 再看「一句話摘要」
- 最後看「最重要的下一步」

## 每天建議節奏

- 早上：更新或建立今天的代理日報
- 中午或下午：補一次重要進展與風險
- 收工前：重建 dashboard data，確認首頁是當天最新版本

## 如果自動刷新沒成功

- 先看 GitHub Actions 的 `Refresh Dashboard Data`
- 確認 repository workflow permissions 允許寫入內容
- 若 workflow 有跑但首頁沒變，先確認 `dashboard/data/latest.json` 是否已更新
