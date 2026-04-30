#!/usr/bin/env python3
"""
Refresh official German legal source snapshots for the german-works-council-law skill.

The script downloads statute HTML pages from gesetze-im-internet.de, stores raw HTML,
and writes cleaned Markdown snapshots into references/generated/.
"""

from __future__ import annotations

import html
import re
import subprocess
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


@dataclass(frozen=True)
class Source:
    filename: str
    title: str
    url: str
    notes: str
    format: str = "html"


SOURCES = [
    Source(
        filename="betrvg.md",
        title="Betriebsverfassungsgesetz (BetrVG)",
        url="https://www.gesetze-im-internet.de/betrvg/BJNR000130972.html",
        notes="Core works council statute.",
    ),
    Source(
        filename="wo-betrvg.md",
        title="Wahlordnung zum Betriebsverfassungsgesetz (WO)",
        url="https://www.gesetze-im-internet.de/betrvgdv1wo/BJNR349400001.html",
        notes="Election-procedure regulation for works council elections.",
    ),
    Source(
        filename="agg.md",
        title="Allgemeines Gleichbehandlungsgesetz (AGG)",
        url="https://www.gesetze-im-internet.de/agg/BJNR189710006.html",
        notes="Equal-treatment and discrimination overlap.",
    ),
    Source(
        filename="arbzg.md",
        title="Arbeitszeitgesetz (ArbZG)",
        url="https://www.gesetze-im-internet.de/arbzg/BJNR117100994.html",
        notes="Working-time overlap.",
    ),
    Source(
        filename="arbschg.md",
        title="Arbeitsschutzgesetz (ArbSchG)",
        url="https://www.gesetze-im-internet.de/arbschg/BJNR124610996.html",
        notes="Health-and-safety overlap.",
    ),
    Source(
        filename="bdsg.md",
        title="Bundesdatenschutzgesetz (BDSG)",
        url="https://www.gesetze-im-internet.de/bdsg_2018/BJNR209710017.html",
        notes="Employee-data and privacy overlap.",
    ),
    Source(
        filename="gdpr.md",
        title="Datenschutz-Grundverordnung (GDPR / DSGVO)",
        url="https://publications.europa.eu/resource/oj/JOL_2016_119_R_0001.DEU.pdfa1a.l_11920160504de00010088.pdf",
        notes="Official German GDPR text from the Publications Office of the European Union.",
        format="pdf",
    ),
]

SKILL_DIR = Path(__file__).resolve().parent.parent
REFERENCES_DIR = SKILL_DIR / "references"
GENERATED_DIR = REFERENCES_DIR / "generated"
RAW_DIR = REFERENCES_DIR / "raw"

MAIN_CONTENT_START = '<div id="paddingLR12">'
MAIN_CONTENT_END = '<div id="footer">'
BLOCK_TAGS = {
    "p",
    "div",
    "table",
    "tr",
    "ul",
    "ol",
    "li",
    "dl",
    "dt",
    "dd",
    "pre",
    "h1",
    "h2",
    "h3",
    "h4",
    "br",
}
SKIP_TAGS = {"script", "style", "map"}


class LawTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._chunks: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag == "br":
            self._chunks.append("\n")
        elif tag == "dt":
            self._chunks.append("\n- ")
        elif tag == "dd":
            self._chunks.append(" ")
        elif tag == "td":
            self._chunks.append(" | ")
        elif tag in BLOCK_TAGS:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
            return
        if self._skip_depth:
            return
        if tag in BLOCK_TAGS:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = data.replace("\xa0", " ")
        text = re.sub(r"\s+", " ", text)
        if text.strip():
            self._chunks.append(text)

    def get_text(self) -> str:
        raw = "".join(self._chunks)
        raw = html.unescape(raw)
        raw = raw.replace("§ ", "§ ")
        lines = [line.strip() for line in raw.splitlines()]
        cleaned: list[str] = []
        blank = False
        for line in lines:
            line = re.sub(r"\s+\|\s+", " | ", line)
            line = re.sub(r"\s{2,}", " ", line).strip()
            if not line:
                if not blank:
                    cleaned.append("")
                blank = True
                continue
            cleaned.append(line)
            blank = False
        return "\n".join(cleaned).strip() + "\n"


def fetch_html(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Codex skill updater for local legal references",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read()
        charset = response.headers.get_content_charset() or "iso-8859-1"
    return content.decode(charset, errors="replace")


def fetch_binary(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Codex skill updater for local legal references",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def extract_main_content(full_html: str) -> str:
    start = full_html.find(MAIN_CONTENT_START)
    if start == -1:
        return full_html
    end = full_html.find(MAIN_CONTENT_END, start)
    if end == -1:
        end = len(full_html)
    return full_html[start:end]


def html_to_text(main_html: str) -> str:
    parser = LawTextParser()
    parser.feed(main_html)
    return parser.get_text()


def pdf_to_text(pdf_path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    lines = [line.rstrip() for line in result.stdout.splitlines()]
    cleaned: list[str] = []
    blank = False
    for line in lines:
        line = re.sub(r"\s{2,}", " ", line).strip()
        if not line:
            if not blank:
                cleaned.append("")
            blank = True
            continue
        cleaned.append(line)
        blank = False
    return "\n".join(cleaned).strip() + "\n"


def build_markdown(source: Source, text: str, retrieved_at: str) -> str:
    return (
        f"# {source.title}\n\n"
        f"- Source: {source.url}\n"
        f"- Retrieved: {retrieved_at}\n"
        f"- Notes: {source.notes}\n\n"
        "> Generated from the official German source. Refresh with `python3 scripts/update_sources.py`.\n\n"
        "## Snapshot\n\n"
        f"{text}"
    )


def main() -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    retrieved_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    for source in SOURCES:
        if source.format == "html":
            full_html = fetch_html(source.url)
            raw_path = RAW_DIR / source.filename.replace(".md", ".html")
            raw_path.write_text(full_html, encoding="utf-8")

            main_html = extract_main_content(full_html)
            text = html_to_text(main_html)
        elif source.format == "pdf":
            raw_path = RAW_DIR / source.filename.replace(".md", ".pdf")
            raw_path.write_bytes(fetch_binary(source.url))
            text = pdf_to_text(raw_path)
        else:
            raise ValueError(f"Unsupported format: {source.format}")

        markdown = build_markdown(source, text, retrieved_at)

        output_path = GENERATED_DIR / source.filename
        output_path.write_text(markdown, encoding="utf-8")
        print(f"[ok] wrote {output_path}")


if __name__ == "__main__":
    main()
