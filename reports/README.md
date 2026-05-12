# Reports

這個目錄存放各代理的每日報告。

## 命名規則

- 路徑：`reports/{agent_name}/YYYY-MM-DD.md`
- 日期格式：`YYYY-MM-DD`
- `agent_name` 請使用穩定、可重複的英文或 kebab-case 名稱
- 每個 agent 只維護自己的資料夾
- frontmatter `agent_name` 必須和資料夾名稱一致
- frontmatter `report_date` 必須和檔名日期一致

## 範例

- `reports/research-agent/2026-05-12.md`
- `reports/calendar-agent/2026-05-12.md`

## 模板

- 請從 `reports/_template/AGENT_NAME/YYYY-MM-DD.md` 複製
- 若代理有額外欄位，可加在 `## 補充欄位` 區塊，不要改掉主要骨架
- 統一規範請看 `docs/agent-report-contract.md`
