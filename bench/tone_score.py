#!/usr/bin/env python3
"""數 AI 味。規則直接對應 SKILL.md 的「AI 味速查」與 prose-style.md 的四個量化上限。

用法：
  python3 bench/tone_score.py bench/out-gen-none.txt bench/out-gen-new.txt
  python3 bench/tone_score.py --detail bench/out-gen-new.txt   # 印出命中的原句

計分是循環的：拿 skill 自己的清單去評 skill 的產出，本來就對 skill 有利。
報告要寫明這點。可信的地方在於清單是公開的，別人可以自己核對每一條。

另外印字數。刪光內容也能讓違規數歸零，所以字數要一起看 —— 字數掉一半而
違規歸零，那不是文筆變好，是內容被砍了。
"""
import pathlib
import re
import sys

# 一看到就刪（SKILL.md「AI 味速查」）
DELETE = [
    "值得注意的是", "需要注意的是", "值得一提的是", "更重要的是", "事實上",
    "毫無疑問", "可以說", "簡單來說", "總的來說", "綜上所述",
    "一句話：", "核心理念：", "關鍵：", "以下是",
]
# 一看到就換
REPLACE = [
    "賦能", "深入探討", "揭示了", "打造", "旨在", "至關重要", "不可或缺",
]
# 開場與收場公式
FORMULA = [
    "這是一個很好的問題", "很好的問題", "當然可以", "希望這些資訊對你有幫助",
    "希望對你有幫助", "總結來說", "讓我們", "首先，我們",
]
# 中國軟體圈行話（語氣的一部分：套語感）
# 「賦能」不放這裡 —— 它已經在 REPLACE，同一個詞不能算兩次
JARGON = ["落地", "閉環", "抓手", "顆粒度", "對齊一下", "痛點"]

PATTERNS = {
    "進行+動詞": re.compile(r"進行(?!式)[一-鿿]{2}"),
    "框式介詞": re.compile(r"在[^，。！？]{1,12}(的過程中|方面)"),
    "假對比": re.compile(r"不是[^，。！？]{1,20}，\s*而是"),
    "三項式排比": re.compile(r"更[一-鿿]{1,3}、\s*更[一-鿿]{1,3}、\s*更"),
    # 破折號的字碼不只一種：全形 U+2014 連用是標準寫法，但模型也會打成
    # U+2500 box drawing（──）或 U+2013、U+2015。只認 —— 會漏掉，實測就漏過
    # 一整篇。這裡收任何 2 個以上的長橫線連用。
    "破折號": re.compile(r"[–—―─]{2,}"),
    "整句加粗": re.compile(r"^\s*\*\*[^*\n]{6,}\*\*\s*$", re.MULTILINE),
    "贅詞一個": re.compile(r"[一][個種位項](?![人二三四五六七八九十])"),
}
# 每千字上限，超過才算違規；其餘規則出現即違規
CAPPED = {"破折號": 1, "假對比": 1, "贅詞一個": 2}


def zh_len(text):
    return len(re.findall(r"[一-鿿]", text)) or 1


def analyse(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    chars = zh_len(text)
    scale = chars / 1000
    hits, total = {}, 0

    for name, words in (("刪除清單", DELETE), ("替換表", REPLACE),
                        ("開場收場公式", FORMULA), ("軟體圈行話", JARGON)):
        found = [w for w in words if w in text]
        if found:
            hits[name] = found
            total += sum(text.count(w) for w in found)

    for name, pat in PATTERNS.items():
        found = pat.findall(text)
        n = len(found)
        if not n:
            continue
        cap = CAPPED.get(name)
        excess = n - round(cap * scale) if cap else n
        if excess > 0:
            hits[name] = [f"{n} 次" + (f"（每千字上限 {cap}）" if cap else "")]
            total += excess

    return {"path": path, "chars": chars, "total": total, "hits": hits, "text": text}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    detail = "--detail" in sys.argv
    if not args:
        sys.exit(__doc__)

    results = [analyse(p) for p in args]
    width = max(len(pathlib.Path(r["path"]).name) for r in results) + 2

    print(f"{'檔案':<{width}}{'中文字數':>9}{'違規':>7}{'每千字':>9}")
    for r in results:
        per_k = r["total"] / (r["chars"] / 1000)
        print(f"{pathlib.Path(r['path']).name:<{width}}{r['chars']:>9}{r['total']:>7}{per_k:>9.1f}")

    for r in results:
        if not r["hits"]:
            continue
        print(f"\n--- {pathlib.Path(r['path']).name} ---")
        for name, found in r["hits"].items():
            print(f"  {name}：{'、'.join(found)}")
            if detail:
                for w in found:
                    if w.endswith("次") or "上限" in w:
                        continue
                    for line in r["text"].splitlines():
                        if w in line:
                            print(f"      {line.strip()[:70]}")


if __name__ == "__main__":
    main()
