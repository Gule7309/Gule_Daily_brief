# Agent Report Contract

## 目的

所有 agent 都用同一種路徑、同一組欄位、同一個摘要區塊寫日報，讓 dashboard 可以自動聚合，不需要對不同 agent 做特殊判斷。

## 每個 agent 必須遵守的規則

1. 只寫入自己的資料夾
2. 路徑固定使用 `reports/{agent_name}/YYYY-MM-DD.md`
3. `agent_name` 使用固定英文名稱或 kebab-case
4. frontmatter 的 `agent_name` 必須和資料夾名稱一致
5. frontmatter 的 `report_date` 必須和檔名日期一致
6. 同一天同一 agent 只保留一份主日報
7. 不要改掉固定章節名稱

## 固定 frontmatter

```yaml
agent_name: your-agent-name
report_date: YYYY-MM-DD
status: on_track
confidence: medium
source_type: daily_report
```

## 固定章節

- `## 今日重點`
- `## 風險與阻塞`
- `## 待跟進事項`
- `## 已完成或已更新事項`
- `## 給總覽儀表板的摘要`
- `## 補充欄位`

## 對 dashboard 最重要的欄位

在 `## 給總覽儀表板的摘要` 裡，至少要填：

- `最新狀態`
- `一句話摘要`
- `最重要的下一步`
- `是否影響今天行程`

## 推薦做法

- 先用 `python3 scripts/new_report.py --agent your-agent-name` 建立日報
- 更新完日報後執行 `python3 scripts/build_dashboard.py`
- push 後由 GitHub Actions 自動刷新 `dashboard/data/latest.json`
