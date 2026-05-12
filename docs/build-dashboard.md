# Build Dashboard

## 用途

把 `reports/` 裡的各代理日報聚合成儀表板可直接讀取的 JSON。

## 執行方式

- `python3 scripts/build_dashboard.py`
- `python3 scripts/build_dashboard.py --date 2026-05-12`

## 輸入

- 預設讀取 `reports/{agent_name}/YYYY-MM-DD.md`
- 若指定日期沒有報告，會退回該代理最近一次可用報告

## 輸出

- `dashboard/data/YYYY-MM-DD.json`
- `dashboard/data/latest.json`

## 目前規則

- 優先讀取 frontmatter 的 `agent_name`、`report_date`、`status`、`confidence`
- 依固定章節解析：`今日重點`、`風險與阻塞`、`待跟進事項`、`已完成或已更新事項`、`給總覽儀表板的摘要`
- 若沒有任何報告，輸出空狀態 dashboard
