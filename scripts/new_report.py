#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
DEFAULT_TIMEZONE = "Asia/Taipei"


TEMPLATE = """---
agent_name: {agent_name}
report_date: {report_date}
status: {status}
confidence: {confidence}
source_type: daily_report
---

# 每日報告

## 今日重點

- 標題：
  摘要：
  原因：
  下一步：

## 風險與阻塞

- 風險描述：
  影響範圍：
  是否需要人工介入：
  建議處理：

## 待跟進事項

- 項目：
  建議跟進時間：
  依賴條件：

## 已完成或已更新事項

- 項目：
  更新內容：
  影響：

## 給總覽儀表板的摘要

- 最新狀態：
- 一句話摘要：
- 最重要的下一步：
- 是否影響今天行程：

## 補充欄位

- 需要時再新增，但請保留以上區塊順序
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a daily agent report from the standard template."
    )
    parser.add_argument("--agent", required=True, help="Agent name in kebab-case")
    parser.add_argument(
        "--date",
        help="Report date in YYYY-MM-DD. Defaults to today in Asia/Taipei.",
    )
    parser.add_argument("--status", default="on_track", help="Initial status value")
    parser.add_argument(
        "--confidence", default="medium", help="Initial confidence value"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the report file if it already exists",
    )
    return parser.parse_args()


def default_date() -> str:
    return datetime.now(ZoneInfo(DEFAULT_TIMEZONE)).strftime("%Y-%m-%d")


def ensure_date(value: str) -> str:
    datetime.strptime(value, "%Y-%m-%d")
    return value


def build_report_path(agent_name: str, report_date: str) -> Path:
    return REPORTS_DIR / agent_name / f"{report_date}.md"


def main() -> None:
    args = parse_args()
    report_date = ensure_date(args.date or default_date())
    target = build_report_path(args.agent, report_date)
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and not args.force:
        raise SystemExit(
            f"Report already exists: {target}. Use --force if you want to overwrite it."
        )

    content = TEMPLATE.format(
        agent_name=args.agent,
        report_date=report_date,
        status=args.status,
        confidence=args.confidence,
    )
    target.write_text(content, encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
