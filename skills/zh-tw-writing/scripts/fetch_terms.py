"""Regenerate references/terms.csv from two sources.

  glossary  Wikibooks《大陸台灣計算機術語對照表》 -- en/tw/cn concept mapping,
            cn column in *simplified* glyphs. Needs requests + bs4 + lxml.
  ruleset   sysprog21/zhtw-mcp assets/ruleset.json -- error->correction rules,
            cn column in *traditional* glyphs, with disambiguation clues.
            Stdlib only.

The two glyph conventions are why both sources stay: grepping 「數據」 misses the
Wikibooks row (which stores 数据) but hits the ruleset row, and vice versa.

--source lets one side be refreshed alone; rows of the other side are carried
over from the checked-in CSV, keyed on the type column. That matters because
the Wikibooks scrape is the fragile half and the checked-in glossary rows hold
hand-written sense qualifiers ("Comment (code)", "Flush (align)",
"Token (security/currency)") that a re-scrape drops. Diff before overwriting.

Rowspan matters in the Wikibooks table: when one English term has several
senses the source merges the English cell across rows. A naive reader sees a
2-cell row and pads it on the right, which shifts every value one column left
-- the tw column then holds simplified Chinese, i.e. the exact mistake this
skill exists to prevent. _expand_row carries merged cells down.

The direction of the cn column is not uniform across rule types, so type is
part of the output and must be read alongside it: for `confusable` rows the cn
column holds a *Taiwan* word used in the wrong sense (函式 is correct in
programming, wrong in maths), and for `disabled` rows the pair is recorded
precisely so it is NOT flagged.
"""
from __future__ import annotations

import argparse
import csv
import json
import urllib.request
from pathlib import Path

WIKIBOOKS_URL = "https://zh.wikibooks.org/zh-tw/%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8"
RULESET_URL = "https://raw.githubusercontent.com/sysprog21/zhtw-mcp/main/assets/ruleset.json"
OUTPUT = Path(__file__).resolve().parent.parent / "references" / "terms.csv"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"

COLUMNS = ["en", "tw", "cn", "type", "clues", "avoid_clues", "note"]
GLOSSARY_TYPE = "glossary"
# ai_filler and translationese are deliberately excluded: SKILL.md keeps its own
# curated AI-tone tables, and zhtw-mcp's filler list deletes words that are
# ordinary in technical prose (此外, 提升, 促進, 隨著, 增強, 維度).
RULE_TYPES = {"cross_strait", "confusable", "political_coloring", "variant"}
SEP = "；"


# --- Wikibooks glossary -----------------------------------------------------


def _normalize_cell(text: str) -> str:
    # Merge multi-line or <br> separated entries into one string.
    parts = [part.strip() for part in text.split("\n") if part.strip()]
    return "; ".join(parts)


def _expand_row(tr, ncols: int, pending: dict[int, tuple[int, str]]) -> list[str]:
    """Return one row as ncols cells, filling in cells carried down by rowspan.

    pending maps column index -> (rows still to fill, text) and is mutated
    across calls, so iterate rows in document order.
    """
    cells = iter(tr.find_all(["th", "td"]))
    out: list[str] = []
    for col in range(ncols):
        if col in pending:
            left, text = pending[col]
            out.append(text)
            if left - 1 > 0:
                pending[col] = (left - 1, text)
            else:
                del pending[col]
            continue
        cell = next(cells, None)
        if cell is None:
            out.append("")
            continue
        text = _normalize_cell(cell.get_text("\n", strip=True))
        span = int(cell.get("rowspan") or 1)
        if span > 1:
            pending[col] = (span - 1, text)
        out.append(text)
    return out


def fetch_glossary() -> list[dict[str, str]]:
    import requests  # imported here so --source ruleset needs no third-party deps
    from bs4 import BeautifulSoup

    resp = requests.get(WIKIBOOKS_URL, headers={"User-Agent": UA}, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class": "wikitable"})
    if table is None:
        raise SystemExit("No wikitable found on page")

    rows = table.find_all("tr")
    if not rows:
        raise SystemExit("No rows found in wikitable")

    raw_headers = [cell.get_text(strip=True) for cell in rows[0].find_all(["th", "td"])]
    columns = ["en", "tw", "cn"][: len(raw_headers)]

    pending: dict[int, tuple[int, str]] = {}
    out: list[dict[str, str]] = []
    for row in rows[1:]:
        cells = _expand_row(row, len(columns), pending)
        if not any(cells):
            continue
        # Every column is filled even though the glossary has no clues: merge()
        # and the writer both index the full set, and a missing key here is a
        # KeyError two functions away.
        record = {col: "" for col in COLUMNS}
        record.update(zip(columns, cells))
        record["type"] = GLOSSARY_TYPE
        out.append(record)

    shifted = [r for r in out if r["en"] and not r["en"].isascii()]
    if shifted:
        raise SystemExit(
            f"{len(shifted)} row(s) have non-ASCII in the en column, e.g. {shifted[0]}. "
            "The table layout changed -- check rowspan handling before overwriting terms.csv."
        )
    return out


# --- zhtw-mcp ruleset -------------------------------------------------------


def _strip_domain(context: str) -> str:
    """Drop the '@domain X。' prefix, which is boilerplate on ~1,000 rules.

    A context that is nothing but the prefix becomes empty, so the note column
    only ever carries something a reader could not infer from the pair itself.
    """
    text = (context or "").strip()
    if text.startswith("@domain"):
        head, sep, tail = text.partition("。")
        text = tail.strip() if sep else ""
    return text


def fetch_ruleset() -> list[dict[str, str]]:
    req = urllib.request.Request(RULESET_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)

    out: list[dict[str, str]] = []
    for rule in data["spelling_rules"]:
        if rule["type"] not in RULE_TYPES:
            continue
        out.append(
            {
                "en": rule.get("english", ""),
                "tw": SEP.join(t for t in rule.get("to", []) if t),
                "cn": rule["from"],
                # A disabled rule is kept on purpose: it records a pair that
                # looks wrong but must not be corrected.
                "type": "disabled" if rule.get("disabled") else rule["type"],
                "clues": SEP.join(rule.get("context_clues", [])),
                "avoid_clues": SEP.join(rule.get("negative_context_clues", [])),
                "note": _strip_domain(rule.get("context", "")),
            }
        )
    return out


# --- merge ------------------------------------------------------------------


def read_existing() -> list[dict[str, str]]:
    if not OUTPUT.exists():
        return []
    with OUTPUT.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = [{col: row.get(col, "") or "" for col in COLUMNS} for row in reader]

    # Carried-over rows are written back out unread, so a mangled file would be
    # laundered into the regenerated table. Check the shape before trusting it.
    if not {"en", "tw", "cn"} <= set(header):
        raise SystemExit(
            f"{OUTPUT} is missing the en/tw/cn columns (found {header}). "
            "Run with --source both to rebuild from scratch."
        )
    blank = [i for i, row in enumerate(rows, 2) if not row["cn"] and not row["tw"]]
    if blank:
        raise SystemExit(
            f"{OUTPUT} has {len(blank)} row(s) with neither cn nor tw, first at line {blank[0]}. "
            "Fix or delete the file before regenerating."
        )

    # The pre-merge CSV had no type column; every one of its rows was glossary.
    for row in rows:
        row["type"] = row["type"] or GLOSSARY_TYPE
    return rows


def _is_informative(row: dict[str, str]) -> bool:
    return bool(row["clues"] or row["avoid_clues"] or row["note"] or row["type"] == "disabled")


def merge(glossary: list[dict[str, str]], ruleset: list[dict[str, str]]) -> list[dict[str, str]]:
    """All surviving glossary rows first, then all surviving ruleset rows.

    Deduping is on the exact (cn, tw) pair. Two rows sharing a cn value but
    disagreeing on tw are different senses and both are kept.

    Cross-source collisions only happen where the mainland term is spelled the
    same in both scripts (文件, 支持, 信息, 接口 -- 17 rows today). 数据 and 數據
    are different keys and both survive on purpose, so that a grep in either
    script finds something. This is a partial dedup by design, not a full one.

    On a collision the informative row wins. The case that forces this is
    文件/檔案: the glossary states it flatly, while the ruleset row is the
    disabled one carrying "裸詞歧義無法消歧" -- keeping the flat row would turn a
    recorded false positive back into a correction.

    The loser is dropped rather than overwritten in place, which keeps the two
    blocks contiguous and the output idempotent. Overwriting would move a row
    across the block boundary, so the next --source run (which carries the
    other block over from this file) would emit the same rows in a different
    order and produce a whole-file diff.
    """
    ruleset_wins = {
        (row["cn"], row["tw"]) for row in ruleset if _is_informative(row)
    }
    kept_glossary = [
        row
        for row in glossary
        if (row["cn"], row["tw"]) not in ruleset_wins or _is_informative(row)
    ]

    seen = {(row["cn"], row["tw"]) for row in kept_glossary}
    kept_ruleset: list[dict[str, str]] = []
    at: dict[tuple[str, str], int] = {}
    for row in ruleset:
        key = (row["cn"], row["tw"])
        if key in seen:
            # Already settled against the glossary block; nothing to weigh up.
            continue
        if key in at:
            # Upstream has no intra-ruleset duplicates today, but if one appears
            # the informative row must win rather than whichever came first in
            # the JSON -- otherwise a later `disabled` override is dropped.
            here = at[key]
            if _is_informative(row) and not _is_informative(kept_ruleset[here]):
                kept_ruleset[here] = row
            continue
        at[key] = len(kept_ruleset)
        kept_ruleset.append(row)
    return kept_glossary + kept_ruleset


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        choices=["both", "glossary", "ruleset"],
        default="both",
        help="Which source to refetch; the other side is carried over from the checked-in CSV",
    )
    args = parser.parse_args()

    existing = read_existing()
    carried = {
        "glossary": [r for r in existing if r["type"] == GLOSSARY_TYPE],
        "ruleset": [r for r in existing if r["type"] != GLOSSARY_TYPE],
    }

    glossary = fetch_glossary() if args.source in ("both", "glossary") else carried["glossary"]
    ruleset = fetch_ruleset() if args.source in ("both", "ruleset") else carried["ruleset"]

    if not glossary or not ruleset:
        raise SystemExit(
            f"Refusing to write a half-empty table (glossary={len(glossary)}, ruleset={len(ruleset)}). "
            "Run with --source both once to rebuild from scratch."
        )

    rows = merge(glossary, ruleset)

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        # csv defaults to CRLF, which would rewrite every line and bury the real
        # changes in the diff. The checked-in file is LF.
        writer = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in COLUMNS})

    print(f"Saved {len(rows)} rows to {OUTPUT} (glossary {len(glossary)}, ruleset {len(ruleset)})")


if __name__ == "__main__":
    main()
