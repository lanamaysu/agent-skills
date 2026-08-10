#!/usr/bin/env python3
"""把三個 arm 的生成題輸出打散成盲測卷。

用法：
  python3 bench/blind.py          # 產生 blind.md（要看的）與 blind-key.txt（別看）
  python3 bench/blind.py G1=B G2=A G3=C   # 對答案

每題兩個版本標成 A／B，順序每題重洗。選完再對答案。

檔名前綴預設 out，要看別組結果就設 BENCH_PREFIX=haiku。
"""
import os
import pathlib
import random
import re
import sys

HERE = pathlib.Path(__file__).parent
ARMS = ["none", "new"]
ARM_LABEL = {"none": "沒有 skill", "new": "有 skill"}
CHOICES = ["A", "B"]
# 種子固定，重跑 blind.py 不會換牌，答案對得起來
SEED = 20260810


def split_tasks(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    parts = re.split(r"^##\s*(G\d)\s*$", text, flags=re.MULTILINE)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


PREFIX = os.environ.get("BENCH_PREFIX", "out")


def build():
    outputs = {}
    for arm in ARMS:
        path = HERE / f"{PREFIX}-gen-{arm}.txt"
        if not path.exists():
            sys.exit(f"缺 {path.name}，先跑 ./bench/run.sh gen")
        outputs[arm] = split_tasks(path)

    task_ids = sorted(set().union(*(o.keys() for o in outputs.values())))
    if not task_ids:
        sys.exit("輸出檔裡找不到 ## G1 之類的標題，先確認格式")

    rng = random.Random(SEED)
    sheet, key = ["# 生成題盲測\n", "每題挑一個你最想直接拿去用的版本，記下代號，選完再跑對答案。\n"], []
    for tid in task_ids:
        # 每題獨立重洗。只有兩個 arm 時不能再要求「不同於上一題」——
        # 那會退化成嚴格交替，看兩題就能推出全部答案。
        order = ARMS[:]
        rng.shuffle(order)
        sheet.append(f"\n---\n\n## {tid}\n")
        for choice, arm in zip(CHOICES, order):
            body = outputs[arm].get(tid, "(這個 arm 沒產出這題)")
            sheet.append(f"\n### {choice}\n\n{body}\n")
            key.append(f"{tid} {choice} = {ARM_LABEL[arm]}")

    (HERE / "blind.md").write_text("\n".join(sheet), encoding="utf-8")
    (HERE / "blind-key.txt").write_text("\n".join(key) + "\n", encoding="utf-8")
    print("blind.md 寫好了，看它、選完再回來對答案：")
    print("  python3 bench/blind.py G1=A G2=B G3=A")


def reveal(picks):
    key = {}
    for line in (HERE / "blind-key.txt").read_text(encoding="utf-8").splitlines():
        tid, choice, _, arm = line.split(" ", 3)
        key[(tid, choice)] = arm

    tally = {}
    for pick in picks:
        tid, _, choice = pick.partition("=")
        arm = key.get((tid.strip(), choice.strip().upper()))
        if arm is None:
            sys.exit(f"對不上：{pick}")
        tally[arm] = tally.get(arm, 0) + 1
        print(f"{tid} 你選了 {choice} -> {arm}")
    print("\n合計：" + "　".join(f"{a} {n}" for a, n in sorted(tally.items())))


if __name__ == "__main__":
    reveal(sys.argv[1:]) if len(sys.argv) > 1 else build()
