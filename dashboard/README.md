# Dashboard

這個目錄放儀表板會直接使用的結構化資料。

## 目錄用途

- `schema/`: 固定 dashboard 骨架與欄位定義
- `examples/`: 參考輸出
- `data/`: 每日實際輸出內容

## 建議輸出檔名

- `dashboard/data/YYYY-MM-DD.json`
- 如果需要保留最新版本別名，可另外寫入 `dashboard/data/latest.json`
