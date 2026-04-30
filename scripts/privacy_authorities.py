#!/usr/bin/env python3
"""
Extract a focused first-pass set of privacy authorities for works-council questions.

The script prints curated bundles of relevant provisions from BetrVG, BDSG, and GDPR
for recurring privacy-heavy topics such as monitoring, AI/profiling, or data access.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
GENERATED_DIR = SKILL_DIR / "references" / "generated"


@dataclass(frozen=True)
class Authority:
    ref: str
    file: str
    kind: str
    number: str
    note: str


TOPICS: dict[str, list[Authority]] = {
    "monitoring": [
        Authority("§ 79a BetrVG", "betrvg.md", "paragraph", "79a", "Works council data-processing baseline."),
        Authority("§ 87 BetrVG", "betrvg.md", "paragraph", "87", "Co-determination hook for technical monitoring."),
        Authority("§ 26 BDSG", "bdsg.md", "paragraph", "26", "Employee-data processing baseline."),
        Authority("Art. 5 GDPR", "gdpr.md", "article", "5", "Core data-processing principles."),
        Authority("Art. 6 GDPR", "gdpr.md", "article", "6", "Lawful bases."),
        Authority("Art. 13 GDPR", "gdpr.md", "article", "13", "Transparency when data is collected."),
        Authority("Art. 15 GDPR", "gdpr.md", "article", "15", "Access requests."),
        Authority("Art. 30 GDPR", "gdpr.md", "article", "30", "Records of processing."),
        Authority("Art. 32 GDPR", "gdpr.md", "article", "32", "Security of processing."),
        Authority("Art. 35 GDPR", "gdpr.md", "article", "35", "DPIA trigger."),
    ],
    "ai-profiling": [
        Authority("§ 79a BetrVG", "betrvg.md", "paragraph", "79a", "Works council privacy baseline."),
        Authority("§ 87 BetrVG", "betrvg.md", "paragraph", "87", "Co-determination hook where systems evaluate behavior or performance."),
        Authority("§ 26 BDSG", "bdsg.md", "paragraph", "26", "Employment-context processing."),
        Authority("Art. 5 GDPR", "gdpr.md", "article", "5", "Principles."),
        Authority("Art. 6 GDPR", "gdpr.md", "article", "6", "Lawful bases."),
        Authority("Art. 9 GDPR", "gdpr.md", "article", "9", "Special-category data."),
        Authority("Art. 22 GDPR", "gdpr.md", "article", "22", "Automated decisions and profiling."),
        Authority("Art. 24 GDPR", "gdpr.md", "article", "24", "Controller responsibility."),
        Authority("Art. 25 GDPR", "gdpr.md", "article", "25", "Privacy by design/default."),
        Authority("Art. 30 GDPR", "gdpr.md", "article", "30", "Processing records."),
        Authority("Art. 35 GDPR", "gdpr.md", "article", "35", "DPIA."),
        Authority("Art. 88 GDPR", "gdpr.md", "article", "88", "Employment-context specificity."),
    ],
    "health-data": [
        Authority("§ 79a BetrVG", "betrvg.md", "paragraph", "79a", "Works council privacy baseline."),
        Authority("§ 26 BDSG", "bdsg.md", "paragraph", "26", "Employee-data baseline, including special-category processing."),
        Authority("Art. 5 GDPR", "gdpr.md", "article", "5", "Principles."),
        Authority("Art. 6 GDPR", "gdpr.md", "article", "6", "Lawful bases."),
        Authority("Art. 9 GDPR", "gdpr.md", "article", "9", "Special-category data."),
        Authority("Art. 32 GDPR", "gdpr.md", "article", "32", "Security."),
        Authority("Art. 35 GDPR", "gdpr.md", "article", "35", "DPIA."),
    ],
    "access-request": [
        Authority("§ 79a BetrVG", "betrvg.md", "paragraph", "79a", "Works council privacy baseline."),
        Authority("§ 26 BDSG", "bdsg.md", "paragraph", "26", "Employment-context processing."),
        Authority("Art. 13 GDPR", "gdpr.md", "article", "13", "Information at collection."),
        Authority("Art. 14 GDPR", "gdpr.md", "article", "14", "Information when data was not collected directly."),
        Authority("Art. 15 GDPR", "gdpr.md", "article", "15", "Access."),
        Authority("Art. 17 GDPR", "gdpr.md", "article", "17", "Erasure overlap when requested."),
    ],
    "retention-deletion": [
        Authority("§ 79 BetrVG", "betrvg.md", "paragraph", "79", "Confidentiality duties."),
        Authority("§ 79a BetrVG", "betrvg.md", "paragraph", "79a", "Privacy baseline."),
        Authority("§ 26 BDSG", "bdsg.md", "paragraph", "26", "Employment-context processing."),
        Authority("Art. 5 GDPR", "gdpr.md", "article", "5", "Storage limitation and data minimization."),
        Authority("Art. 17 GDPR", "gdpr.md", "article", "17", "Erasure."),
        Authority("Art. 30 GDPR", "gdpr.md", "article", "30", "Records."),
        Authority("Art. 32 GDPR", "gdpr.md", "article", "32", "Security."),
    ],
    "works-council-data": [
        Authority("§ 79 BetrVG", "betrvg.md", "paragraph", "79", "Confidentiality."),
        Authority("§ 79a BetrVG", "betrvg.md", "paragraph", "79a", "Works council data-processing rule."),
        Authority("§ 26 BDSG", "bdsg.md", "paragraph", "26", "Employment-context processing."),
        Authority("Art. 5 GDPR", "gdpr.md", "article", "5", "Principles."),
        Authority("Art. 6 GDPR", "gdpr.md", "article", "6", "Lawful bases."),
        Authority("Art. 24 GDPR", "gdpr.md", "article", "24", "Controller responsibility."),
        Authority("Art. 25 GDPR", "gdpr.md", "article", "25", "Privacy by design/default."),
        Authority("Art. 30 GDPR", "gdpr.md", "article", "30", "Records."),
        Authority("Art. 32 GDPR", "gdpr.md", "article", "32", "Security."),
        Authority("Art. 88 GDPR", "gdpr.md", "article", "88", "Employment context."),
    ],
}


def normalize_heading(line: str) -> str:
    line = re.sub(r"^(§\s*\d+[a-z]?)\s*([A-ZÄÖÜ])", r"\1 \2", line)
    return re.sub(r"\s{2,}", " ", line).strip()


def extract_block(text: str, kind: str, number: str) -> str:
    if kind == "paragraph":
        pattern = re.compile(
            rf"^§\s*{re.escape(number)}[a-zA-Z]?(?:\s*[A-ZÄÖÜa-zäöü].*)?$",
            re.MULTILINE,
        )
        next_pattern = re.compile(r"^§\s*\d+[a-zA-Z]?(?:\s*[A-ZÄÖÜa-zäöü].*)?$", re.MULTILINE)
    elif kind == "article":
        pattern = re.compile(
            rf"^Artikel\s+{re.escape(number)}(?:\s*[A-ZÄÖÜa-zäöü].*)?$",
            re.MULTILINE,
        )
        next_pattern = re.compile(r"^Artikel\s+\d+[a-zA-Z]?(?:\s*[A-ZÄÖÜa-zäöü].*)?$", re.MULTILINE)
    else:
        raise ValueError(f"Unsupported kind: {kind}")

    match = pattern.search(text)
    if not match:
        return ""

    start = match.start()
    rest = text[match.end():]
    next_match = next_pattern.search(rest)
    end = match.end() + next_match.start() if next_match else len(text)
    block = text[start:end].strip()

    lines = [normalize_heading(line.rstrip()) for line in block.splitlines()]
    cleaned: list[str] = []
    blank = False
    for line in lines:
        if line == "Nichtamtliches Inhaltsverzeichnis":
            continue
        if not line:
            if not blank:
                cleaned.append("")
            blank = True
            continue
        cleaned.append(line)
        blank = False
    return "\n".join(cleaned).strip()


def print_topics() -> None:
    print("Available topics:")
    for topic in sorted(TOPICS):
        print(f"- {topic}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract focused privacy authorities for WoCo questions.")
    parser.add_argument("--topic", help="Topic bundle to print.")
    parser.add_argument("--list-topics", action="store_true", help="List supported topics.")
    parser.add_argument("--max-chars", type=int, default=2200, help="Trim each extracted authority block to this size.")
    args = parser.parse_args()

    if args.list_topics:
        print_topics()
        return 0

    if not args.topic:
        parser.error("provide --topic or use --list-topics")

    topic = args.topic.strip().lower()
    if topic not in TOPICS:
        print(f"Unknown topic: {topic}", file=sys.stderr)
        print_topics()
        return 2

    print(f"# Privacy Authority Bundle: {topic}\n")
    print("Informational aid only. This output is prone to mistakes and does not replace German-qualified legal advice.\n")

    for authority in TOPICS[topic]:
        path = GENERATED_DIR / authority.file
        text = path.read_text(encoding="utf-8")
        block = extract_block(text, authority.kind, authority.number)
        print(f"## {authority.ref}")
        print(f"Source file: {path}")
        print(f"Why it matters: {authority.note}\n")
        if not block:
            print("[Section not found in generated snapshot]\n")
            continue
        if len(block) > args.max_chars:
            block = block[: args.max_chars].rstrip() + "\n[... trimmed ...]"
        print(block)
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
