#!/usr/bin/env python3
"""由 items.csv 生成兩份術語題提示。改題目只動 items.csv，然後跑這支。

  python3 bench/gen_prompts.py

兩份提示的差別只有第一行：skill arm 指定去讀 SKILL.md，baseline 什麼都不提。
baseline 那行刻意只講「中文」，不講「台灣用語」——講了就等於把 skill 的核心
指令直接餵給對照組，測出來的差異會消失。
"""
import csv
import pathlib

BENCH = pathlib.Path(__file__).parent

HEAD_SKILL = "先讀 ./skills/taiwan-traditional-chinese/SKILL.md，照它的規則處理下面 {n} 句。"
HEAD_NEUTRAL = "請把下面 {n} 句改寫成通順的中文，用詞不當的地方請改掉。不需要修改的句子就原句照抄。"
BODY = """

每句輸出修正後的版本；判斷不需要修正就原句照抄。
只輸出 {n} 行，格式 `編號<TAB>句子`，不要任何說明、標題或前後文。

{lines}
"""


def main():
    with open(BENCH / "items.csv", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    lines = "\n".join(f"{r['id']}\t{r['input']}" for r in rows)
    n = len(rows)
    for head, name in ((HEAD_SKILL, "prompt.md"), (HEAD_NEUTRAL, "prompt-baseline-neutral.md")):
        text = head.format(n=n) + BODY.format(n=n, lines=lines)
        (BENCH / name).write_text(text, encoding="utf-8")
        print(f"寫入 {name}（{n} 句）")


if __name__ == "__main__":
    main()
