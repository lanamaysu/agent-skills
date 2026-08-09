"""Fixture tests for lint_zhtw.py. Run: python3 scripts/test_lint_zhtw.py

Two halves that have to hold together. A linter that reports nothing on this
repository proves nothing on its own -- over-masking looks identical to a clean
result -- so every check is also exercised against text that must trip it.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("lint_zhtw", HERE / "lint_zhtw.py")
lint_zhtw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint_zhtw)

VIOLATIONS = """# 測試

這是一段中文, 用了半形逗號。這句用半形句號. 後面還有字。

這段有兩處**加粗**還有另一處**加粗**，超過上限。

**這整句都被加粗了。**

這裡混進簡體字：数据、组件、服务器。

一段有破折號——這裡一組——這裡第二組——這裡第三組，全部都在同一段裡面而且字數不到一千字。
"""

MASKED = """# 遮罩測試

```bash
grep '数据, 组件' file
```

行內程式碼 `数据, 组件` 也不該被抓。

| 禁用 | 替代 |
|------|------|
| 数据, 组件 | 資料、元件 |

<!-- zhtw-lint: off -->
这里是被抑制的简体, 半形逗號**加粗一**與**加粗二**。
<!-- zhtw-lint: on -->

正常的一句中文，沒有問題。
"""

FRONTMATTER = """---
description: 'mainland wording (數據/組件), jargon (落地/閉環), terms (元件/資料).'
---

正常的一句中文，沒有問題。
"""

UNCLOSED = """# 未關閉

<!-- zhtw-lint: off -->
数据
"""

# A bolded lead-in labels a definition entry and does not spend the paragraph's
# one allowance; a bolded sentence is a violation wherever it sits.
LEAD_IN_OK = "- **prose-style.md**：只在寫散文時讀，其他情況**不要讀**。\n"
LEAD_IN_BAD = "- **prose-style.md**：只在寫散文時讀，其他**不要讀**，再加一處**強調**。\n"
LEAD_IN_SENTENCE = "- **這個標籤本身就是一整句話。**其餘內容。\n"

failures: list[str] = []


def run(text: str, *, terms=None) -> list[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as f:
        f.write(text)
        path = Path(f.name)
    try:
        return [f.check for f in lint_zhtw.lint(path, terms)]
    finally:
        path.unlink()


def expect(name: str, actual, predicate, description: str) -> None:
    if predicate(actual):
        print(f"  ok   {name}")
    else:
        failures.append(f"{name}: expected {description}, got {actual}")
        print(f"  FAIL {name}: expected {description}, got {actual}")


print("positive control -- every check must fire")
checks = run(VIOLATIONS)
for want in ["半形標點", "加粗密度", "整句加粗", "簡體殘留", "破折號密度"]:
    expect(want, checks, lambda c, w=want: w in c, f"{want} to be reported")

print("negative control -- masked regions must stay silent")
expect("code/inline/table/suppressed", run(MASKED), lambda c: c == [], "no findings")
expect("yaml frontmatter", run(FRONTMATTER), lambda c: c == [], "no findings")

print("suppression hygiene")
expect("unclosed off region", run(UNCLOSED), lambda c: c == ["標記錯誤"], "['標記錯誤']")

print("bold lead-in handling")
expect("lead-in + one emphasis", run(LEAD_IN_OK), lambda c: c == [], "no findings")
expect("lead-in + two emphases", run(LEAD_IN_BAD), lambda c: "加粗密度" in c, "加粗密度")
expect("lead-in that is a sentence", run(LEAD_IN_SENTENCE), lambda c: "整句加粗" in c, "整句加粗")

print("adversarial cases from review")
# Half-width punctuation between two CJK characters has no whitespace to anchor
# on; the first version of the regex required it and missed the common case.
expect("halfwidth with no spaces", run("# t\n\n中文,中文。中文:中文。\n"),
       lambda c: c.count("半形標點") == 2, "two 半形標點")
expect("ascii punctuation untouched", run("# t\n\n檔案在 README.md，版本 3.14 沒問題。\n"),
       lambda c: c == [], "no findings")
# A single in_fence flag let a ~~~ line inside a ``` block close it early.
expect("nested fence markers", run("# t\n\n```\n~~~\n中文,中文\n```\n"),
       lambda c: c == [], "no findings")
expect("unclosed fence", run("# t\n\n```bash\necho hi\n"),
       lambda c: c == ["標記錯誤"], "['標記錯誤']")

print("vocabulary check is data-driven, not hard-coded")
# terms.csv has 34 rows whose two sides are identical (容器, 下拉, 框架).
expect("no self-referential 用詞", run("# t\n\n這個容器與下拉選單都用框架實作。\n", terms=lint_zhtw.load_terms()),
       lambda c: "用詞" not in c, "no 用詞")
terms = lint_zhtw.load_terms()
expect("terms.csv loaded", terms, lambda t: len(t) > 1000, "over 1000 entries from terms.csv")
expect("--terms finds 数据", run(VIOLATIONS, terms=terms), lambda c: "用詞" in c, "用詞")
expect("default run skips vocabulary", run(VIOLATIONS), lambda c: "用詞" not in c, "no 用詞")

print("simplified set excludes traditional glyphs seen only on the cn side")
simplified = lint_zhtw.load_simplified_only()
exact = lint_zhtw.simplified_is_exact()
# 崩捆碰 reached this list by audit, not by bug report: scripts/audit_shared_glyphs.py
# diffs the derived set against opencc, so the patch list is complete rather
# than however far real-world usage happened to get.
for ch in "崩捆晰短碰禁答細刻奏":
    expect(f"{ch} not simplified", simplified, lambda s, c=ch: c not in s, f"{ch} absent")
for ch in "数据组务":
    expect(f"{ch} is simplified", simplified, lambda s, c=ch: c in s, f"{ch} present")
# The sentence that caught this: 碰 sits only in 触碰 on the cn side, so nothing
# in the table vouched for it and ordinary prose tripped the check.
expect("shared glyph in real prose", run("# t\n\n元件只要碰到 store 就用輔助函式。\n"),
       lambda c: c == [], "no findings")

if exact:
    print("patch list is complete (opencc available as oracle)")
    derived = {ch for ch in simplified}
    expect("no shared glyph slipped back in", lint_zhtw.SHARED_GLYPHS,
           lambda g: not (g & derived), "SHARED_GLYPHS disjoint from the real simplified set")

if exact:
    expect("织 is simplified (opencc)", simplified, lambda s: "织" in s, "织 present")
else:
    # Documented hole in the fallback: 织 never reaches a glossary cn value, so
    # terms.csv has no evidence for it. Asserted as a known miss rather than
    # ignored, so that installing opencc visibly changes the result.
    expect("织 is a known fallback miss", simplified, lambda s: "织" not in s, "织 absent without opencc")

print()
if failures:
    print(f"{len(failures)} failure(s)")
    sys.exit(1)
print("all assertions passed")
