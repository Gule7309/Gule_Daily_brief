#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
REQUIRED_SECTIONS = [
    "今日重點",
    "風險與阻塞",
    "待跟進事項",
    "已完成或已更新事項",
    "給總覽儀表板的摘要",
]
REQUIRED_FRONTMATTER = ["agent_name", "report_date", "status", "confidence"]


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


def find_sections(body: str) -> set[str]:
    return {
        line[3:].strip()
        for line in body.splitlines()
        if line.startswith("## ")
    }


def iter_reports() -> list[Path]:
    paths: list[Path] = []
    for path in REPORTS_DIR.rglob("*.md"):
        rel = path.relative_to(REPORTS_DIR)
        if rel.parts[0].startswith("_"):
            continue
        if path.name == "README.md":
            continue
        paths.append(path)
    return sorted(paths)


def validate_report(path: Path) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT)
    agent_name = path.parent.name
    filename = path.name

    if not DATE_RE.match(filename):
        errors.append(f"{rel}: filename must use YYYY-MM-DD.md")

    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    for key in REQUIRED_FRONTMATTER:
        if not meta.get(key):
            errors.append(f"{rel}: missing frontmatter field `{key}`")

    if meta.get("agent_name") and meta["agent_name"] != agent_name:
        errors.append(
            f"{rel}: frontmatter agent_name `{meta['agent_name']}` must match folder `{agent_name}`"
        )

    stem = path.stem
    if meta.get("report_date") and meta["report_date"] != stem:
        errors.append(
            f"{rel}: frontmatter report_date `{meta['report_date']}` must match filename `{stem}`"
        )

    sections = find_sections(body)
    for section in REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(f"{rel}: missing section `## {section}`")

    return errors


def main() -> None:
    errors: list[str] = []
    reports = iter_reports()

    for report in reports:
        errors.extend(validate_report(report))

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(f"Validated {len(reports)} report files.")


if __name__ == "__main__":
    main()
