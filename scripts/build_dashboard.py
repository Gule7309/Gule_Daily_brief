#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
DASHBOARD_DIR = ROOT / "dashboard" / "data"
DEFAULT_TIMEZONE = "Asia/Taipei"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")


@dataclass
class Report:
    agent_name: str
    report_date: str
    status: str
    confidence: str
    source_file: str
    summary: str
    next_step: str
    today_highlights: list[dict[str, str]]
    risks: list[dict[str, str]]
    follow_ups: list[dict[str, str]]
    completed: list[dict[str, str]]
    calendar_impact: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate daily agent reports into dashboard JSON."
    )
    parser.add_argument(
        "--date",
        help="Target date in YYYY-MM-DD. Defaults to today in Asia/Taipei.",
    )
    parser.add_argument(
        "--reports-dir",
        default=str(REPORTS_DIR),
        help="Directory containing reports/{agent_name}/YYYY-MM-DD.md",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DASHBOARD_DIR),
        help="Directory for generated dashboard JSON files.",
    )
    return parser.parse_args()


def target_date(value: str | None) -> str:
    if value:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    return datetime.now(ZoneInfo(DEFAULT_TIMEZONE)).strftime("%Y-%m-%d")


def list_reports(reports_dir: Path) -> dict[str, list[Path]]:
    agents: dict[str, list[Path]] = {}
    if not reports_dir.exists():
        return agents

    for agent_dir in reports_dir.iterdir():
        if not agent_dir.is_dir() or agent_dir.name.startswith("_"):
            continue
        files = sorted(
            path for path in agent_dir.iterdir() if path.is_file() and DATE_RE.match(path.name)
        )
        if files:
            agents[agent_dir.name] = files
    return agents


def choose_report(files: Iterable[Path], dashboard_date: str) -> Path | None:
    dated = sorted(files)
    exact = [path for path in dated if path.stem == dashboard_date]
    if exact:
        return exact[-1]

    earlier = [path for path in dated if path.stem <= dashboard_date]
    if earlier:
        return earlier[-1]

    return dated[-1] if dated else None


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text

    raw_meta, body = parts
    meta: dict[str, str] = {}
    for line in raw_meta.splitlines()[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body


def parse_labeled_block(lines: list[str]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            if current:
                items.append(current)
            current = {}
            stripped = stripped[2:].strip()
            if ":" in stripped:
                key, value = stripped.split(":", 1)
                current[key.strip()] = value.strip()
            else:
                current["item"] = stripped
            continue
        if current is None or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        current[key.strip()] = value.strip()

    if current:
        items.append(current)
    return items


def section_map(body: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def first_nonempty(item: dict[str, str], keys: list[str], fallback: str = "") -> str:
    for key in keys:
        value = item.get(key, "").strip()
        if value:
            return value
    return fallback


def parse_report(path: Path) -> Report:
    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    sections = section_map(body)

    highlights = parse_labeled_block(sections.get("今日重點", []))
    risks = parse_labeled_block(sections.get("風險與阻塞", []))
    follow_ups = parse_labeled_block(sections.get("待跟進事項", []))
    completed = parse_labeled_block(sections.get("已完成或已更新事項", []))
    summary_block = parse_labeled_block(sections.get("給總覽儀表板的摘要", []))
    summary_item = summary_block[0] if summary_block else {}

    agent_name = meta.get("agent_name") or path.parent.name
    report_date = meta.get("report_date") or path.stem
    status = first_nonempty(summary_item, ["最新狀態"], meta.get("status", "unknown"))
    summary = first_nonempty(summary_item, ["一句話摘要"], "目前無摘要")
    next_step = first_nonempty(summary_item, ["最重要的下一步"], "目前無下一步")
    calendar_impact = first_nonempty(summary_item, ["是否影響今天行程"], "未知")
    confidence = meta.get("confidence", "medium")

    return Report(
        agent_name=agent_name,
        report_date=report_date,
        status=status,
        confidence=confidence,
        source_file=str(path.relative_to(ROOT)),
        summary=summary,
        next_step=next_step,
        today_highlights=highlights,
        risks=risks,
        follow_ups=follow_ups,
        completed=completed,
        calendar_impact=calendar_impact,
    )


def build_empty_dashboard(dashboard_date: str) -> dict:
    return {
        "date": dashboard_date,
        "top_summary": "目前尚未收到可整理的代理日報，今天先維持空狀態摘要。",
        "key_metrics": {
            "pending_count": 0,
            "blocked_count": 0,
            "completed_count": 0,
            "decision_needed_count": 0,
            "active_agent_count": 0,
        },
        "today_priorities": [
            {
                "title": "目前無更新",
                "source_agent": "system",
                "reason": "尚未讀到任何代理日報",
                "next_step": "將今日報告放入 reports/{agent_name}/YYYY-MM-DD.md",
            }
        ],
        "calendar_alignment": [
            {
                "time_range": "目前無更新",
                "related_event": "目前無事件資料",
                "affected_item": "目前無關聯項目",
                "suggested_priority": "normal",
            }
        ],
        "agent_updates": [
            {
                "agent_name": "system",
                "latest_status": "no_report",
                "summary": "目前尚無代理報告可整理。",
                "next_step": "新增第一份日報後即可開始聚合。",
                "confidence": "high",
                "source_file": "N/A",
                "report_date": dashboard_date,
                "extra": {},
            }
        ],
        "risks_and_alerts": [
            {
                "risk_description": "目前缺少代理日報來源。",
                "impact_scope": "無法產出有內容的每日總覽。",
                "needs_human_intervention": False,
            }
        ],
        "follow_ups": [
            {
                "item": "建立第一份代理日報",
                "owner_source": "agent report source",
                "suggested_follow_up_time": "today",
            }
        ],
    }


def build_dashboard(reports: list[Report], dashboard_date: str) -> dict:
    if not reports:
        return build_empty_dashboard(dashboard_date)

    today_priorities: list[dict[str, str]] = []
    calendar_alignment: list[dict[str, str]] = []
    risks_and_alerts: list[dict[str, object]] = []
    follow_ups: list[dict[str, str]] = []
    agent_updates: list[dict[str, object]] = []

    completed_count = 0
    blocked_count = 0
    pending_count = 0
    decision_needed_count = 0

    for report in sorted(reports, key=lambda item: item.agent_name):
        agent_updates.append(
            {
                "agent_name": report.agent_name,
                "latest_status": report.status,
                "summary": report.summary,
                "next_step": report.next_step,
                "confidence": report.confidence,
                "source_file": report.source_file,
                "report_date": report.report_date,
                "extra": {"calendar_impact": report.calendar_impact},
            }
        )

        for item in report.today_highlights:
            today_priorities.append(
                {
                    "title": first_nonempty(item, ["標題"], "未命名事項"),
                    "source_agent": report.agent_name,
                    "reason": first_nonempty(item, ["原因"], report.summary),
                    "next_step": first_nonempty(item, ["下一步"], report.next_step),
                }
            )

        for item in report.risks:
            impact = first_nonempty(item, ["影響範圍"], "未提供")
            needs_human = first_nonempty(item, ["是否需要人工介入"], "否").lower()
            risks_and_alerts.append(
                {
                    "risk_description": first_nonempty(item, ["風險描述"], "未提供"),
                    "impact_scope": impact,
                    "needs_human_intervention": needs_human in {"是", "yes", "true"},
                }
            )
            blocked_count += 1
            if needs_human in {"是", "yes", "true"}:
                decision_needed_count += 1

        for item in report.follow_ups:
            follow_ups.append(
                {
                    "item": first_nonempty(item, ["項目"], "未命名跟進項"),
                    "owner_source": report.agent_name,
                    "suggested_follow_up_time": first_nonempty(
                        item, ["建議跟進時間"], "today"
                    ),
                }
            )
            pending_count += 1

        completed_count += len(report.completed)

        if report.calendar_impact and report.calendar_impact not in {"否", "無", "未知"}:
            calendar_alignment.append(
                {
                    "time_range": dashboard_date,
                    "related_event": report.calendar_impact,
                    "affected_item": report.summary,
                    "suggested_priority": "high",
                }
            )

    if not today_priorities:
        today_priorities.append(
            {
                "title": "目前無更新",
                "source_agent": "system",
                "reason": "現有日報未提供今日重點",
                "next_step": "補上今日重點區塊",
            }
        )

    if not calendar_alignment:
        calendar_alignment.append(
            {
                "time_range": "目前無更新",
                "related_event": "目前無事件資料",
                "affected_item": "目前無關聯項目",
                "suggested_priority": "normal",
            }
        )

    if not risks_and_alerts:
        risks_and_alerts.append(
            {
                "risk_description": "目前無風險。",
                "impact_scope": "目前無明顯阻塞。",
                "needs_human_intervention": False,
            }
        )

    if not follow_ups:
        follow_ups.append(
            {
                "item": "目前無待跟進事項",
                "owner_source": "system",
                "suggested_follow_up_time": "N/A",
            }
        )

    top_summary = (
        f"今天共有 {len(reports)} 個活躍代理來源，"
        f"{blocked_count} 個阻塞，{pending_count} 個待跟進，"
        f"{completed_count} 個已完成或已更新事項。"
    )

    return {
        "date": dashboard_date,
        "top_summary": top_summary,
        "key_metrics": {
            "pending_count": pending_count,
            "blocked_count": blocked_count,
            "completed_count": completed_count,
            "decision_needed_count": decision_needed_count,
            "active_agent_count": len(reports),
        },
        "today_priorities": today_priorities[:5],
        "calendar_alignment": calendar_alignment,
        "agent_updates": agent_updates,
        "risks_and_alerts": risks_and_alerts,
        "follow_ups": follow_ups,
    }


def main() -> None:
    args = parse_args()
    dashboard_date = target_date(args.date)
    reports_dir = Path(args.reports_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    selected_reports: list[Report] = []
    for _, files in sorted(list_reports(reports_dir).items()):
        chosen = choose_report(files, dashboard_date)
        if chosen:
            selected_reports.append(parse_report(chosen))

    dashboard = build_dashboard(selected_reports, dashboard_date)

    dated_path = output_dir / f"{dashboard_date}.json"
    latest_path = output_dir / "latest.json"

    payload = json.dumps(dashboard, ensure_ascii=False, indent=2) + "\n"
    dated_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")

    print(f"Wrote {dated_path}")
    print(f"Wrote {latest_path}")


if __name__ == "__main__":
    main()
