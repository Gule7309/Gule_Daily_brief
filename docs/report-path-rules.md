# Report Path Rules

## 主規則

- 主資料來源路徑格式：`reports/{agent_name}/YYYY-MM-DD.md`
- 代理名稱使用固定英文名稱或 kebab-case
- 同一代理每日只保留一份主報告

## 篩選順序

1. 優先選取今天日期的報告
2. 若今天沒有，退回最近一次可用日期
3. 若同日多份衝突，優先完整度較高者，並標示衝突

## 模板位置

- `reports/_template/AGENT_NAME/YYYY-MM-DD.md`

## 備註

- 若後續出現少數代理需要額外欄位，請只在 `補充欄位` 擴充，不要改掉主要區塊名稱
