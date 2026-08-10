#!/usr/bin/env python3
"""比對各 arm 的術語題輸出與 items.csv 的答案。

用法：python3 bench/score.py bench/out-terms-*.txt

arm 名稱從檔名推出來（none／old／new）。expected 是標準答案，
also_ok 是同樣算對的替代寫法（分號分隔）。比對前拿掉所有空白，
數字與單位之間有沒有空格不影響判定。
"""
import csv
import pathlib
import re
import sys

ARM_LABEL = {
    "none": "沒有 skill",
    "new": "有 skill",
    "old": "舊版 skill (dbad5b7~1)",
}
STRATUM_LABEL = {
    "common": "常見詞（要改）",
    "obscure": "冷僻詞（要改）",
    "pair-keep": "防守題（不該改）",
    "new": "新詞收錄",
    "new-overreach": "過度修正控制組",
    "pair-fix": "最小對立對（該改）",
}


def norm(text):
    return re.sub(r"\s+", "", text.strip())


def load_items():
    path = pathlib.Path(__file__).parent / "items.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    missing = [r["id"] for r in rows if not r["expected"].strip()]
    if missing:
        sys.exit(f"items.csv 還有 expected 沒填：{', '.join(missing)}")
    return rows


def load_output(path):
    out = {}
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        key, _, text = line.partition("\t")
        out[key.strip()] = text.strip()
    return out


def arm_name(path):
    stem = pathlib.Path(path).stem
    for key, label in ARM_LABEL.items():
        if stem.endswith(key):
            return label
    return stem


def judge(row, got):
    """ok / MISS / OVER。

    只看目標詞：banned 不能出現，required 至少要中一個。整句 exact match 會把
    「整批取消」改寫成「整批復原」這種與題目無關的措辭算成錯，那不是我們要測的。
    """
    text = norm(got)
    banned = norm(row.get("banned", ""))
    required = [norm(w) for w in row.get("required", "").split("；") if w.strip()]

    if (not banned or banned not in text) and any(w in text for w in required):
        return "ok"
    return "OVER" if row["stratum"] in ("pair-keep", "new-overreach") else "MISS"


def score(rows, path):
    out = load_output(path)
    label = arm_name(path)
    marks = {r["id"]: judge(r, out.get(r["id"], "")) for r in rows}
    hit = sum(m == "ok" for m in marks.values())
    over = sum(m == "OVER" for m in marks.values())
    miss = sum(m == "MISS" for m in marks.values())

    print(f"\n=== {label} ===")
    print(f"正確 {hit}/{len(rows)}　漏改 {miss}　過度修正 {over}")
    for stratum, name in STRATUM_LABEL.items():
        group = [r for r in rows if r["stratum"] == stratum]
        if group:
            n = sum(marks[r["id"]] == "ok" for r in group)
            print(f"  {name}：{n}/{len(group)}")
    for r in rows:
        if marks[r["id"]] != "ok":
            print(f"  {r['id']} {marks[r['id']]}: {out.get(r['id'], '(缺這行)')}")
    return label, hit, miss, over


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    rows = load_items()
    results = [score(rows, p) for p in sys.argv[1:]]
    print(f"\n{'arm':<26}{'正確':>6}{'漏改':>6}{'過度修正':>10}")
    for label, hit, miss, over in results:
        print(f"{label:<26}{hit:>6}{miss:>6}{over:>10}")


if __name__ == "__main__":
    main()
