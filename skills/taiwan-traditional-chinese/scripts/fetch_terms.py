"""Regenerate references/terms.csv from the Wikibooks terminology table.

Uses a custom user agent to avoid 403 and normalizes multi-line cells.

Rowspan matters here: when one English term has several senses (Comment,
Flush, Token) the source table merges the English cell across rows. A naive
reader sees a 2-cell row and pads it on the right, which shifts every value
one column left -- the tw column then holds simplified Chinese, i.e. the exact
mistake this skill exists to prevent. _expand_row carries merged cells down.

Multi-sense terms therefore appear as two rows with the same en value. The
checked-in terms.csv adds hand-written sense qualifiers to those rows
("Comment (code)", "Flush (align)", "Token (security/currency)"); regenerating
drops the qualifiers, so diff before overwriting.
"""
from __future__ import annotations

import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://zh.wikibooks.org/zh-tw/%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8"
OUTPUT = Path(__file__).resolve().parent.parent / "references" / "terms.csv"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"


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


def main() -> None:
    resp = requests.get(URL, headers={"User-Agent": UA}, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find("table", {"class": "wikitable"})
    if table is None:
        raise SystemExit("No wikitable found on page")

    rows = table.find_all("tr")
    if not rows:
        raise SystemExit("No rows found in wikitable")

    raw_headers = [cell.get_text(strip=True) for cell in rows[0].find_all(["th", "td"])]
    # Map known headers to canonical column names.
    columns = ["en", "tw", "cn"][: len(raw_headers)]

    pending: dict[int, tuple[int, str]] = {}
    data_rows = []
    for row in rows[1:]:
        cells = _expand_row(row, len(columns), pending)
        if not any(cells):
            continue
        data_rows.append(dict(zip(columns, cells)))

    shifted = [r for r in data_rows if r["en"] and not r["en"].isascii()]
    if shifted:
        raise SystemExit(
            f"{len(shifted)} row(s) have non-ASCII in the en column, e.g. {shifted[0]}. "
            "The table layout changed -- check rowspan handling before overwriting terms.csv."
        )

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        # csv defaults to CRLF, which would rewrite all 465 lines and bury the
        # real changes in the diff. The checked-in file is LF.
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(data_rows)

    print(f"Saved {len(data_rows)} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
