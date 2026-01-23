"""Fetch the Wikibooks terminology table and save it as references/terms.csv.
Uses a custom user agent to avoid 403 and normalizes multi-line cells.
"""
from __future__ import annotations

import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://zh.wikibooks.org/zh-tw/%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8"
OUTPUT = Path(__file__).with_name("terms.csv")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"


def _normalize_cell(text: str) -> str:
    # Merge multi-line or <br> separated entries into one string.
    parts = [part.strip() for part in text.split("\n") if part.strip()]
    return "; ".join(parts)


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

    data_rows = []
    for row in rows[1:]:
        cells = [_normalize_cell(cell.get_text("\n", strip=True)) for cell in row.find_all(["th", "td"])]
        if len(cells) < len(columns):
            cells.extend([""] * (len(columns) - len(cells)))
        data_rows.append(dict(zip(columns, cells)))

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data_rows)

    print(f"Saved {len(data_rows)} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
