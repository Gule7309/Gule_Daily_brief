# Repo Structure

## 目的

讓每日代理報告、聚合邏輯與儀表板輸出有穩定且可比較的目錄結構。

## 建議結構

- `reports/`: 原始代理日報
- `dashboard/schema/`: 穩定輸出 schema
- `dashboard/examples/`: 空狀態或範例輸出
- `dashboard/data/`: 實際提供給本機儀表板的每日 JSON
- `docs/`: 規則與維護文件

## 最小可用流程

1. 各代理寫入 `reports/{agent_name}/YYYY-MM-DD.md`
2. 聚合程序讀取最新報告
3. 依 `dashboard/schema/dashboard-schema.json` 產出每日 JSON
4. 將結果寫到 `dashboard/data/YYYY-MM-DD.json`
