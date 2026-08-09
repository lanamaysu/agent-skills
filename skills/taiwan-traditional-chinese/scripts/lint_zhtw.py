"""Mechanical zh-TW checks for Markdown, for the checks a reader does badly by eye.

Deliberately narrow. Vocabulary, tone and jargon are already covered by the
tables in SKILL.md, which are in the model's context while it writes; re-running
them here mostly produces false positives, because a document that *teaches* the
banned words contains every one of them as a specimen. What a reader cannot do
reliably is count: dashes per thousand characters, bold spans per paragraph,
half-width punctuation buried in a CJK sentence, one stray simplified glyph.

    python3 scripts/lint_zhtw.py <path>...        # the counting checks
    python3 scripts/lint_zhtw.py --terms <path>   # also grep terms.csv vocabulary
    python3 scripts/test_lint_zhtw.py             # fixtures for every check

Exit status is 1 when anything is reported, so it drops into a pre-commit hook
or CI step unchanged.

Excluded from every check: fenced code blocks, inline code spans, link targets,
YAML frontmatter, Markdown table rows (that is where ban tables live), and lines
opening with ❌ / ✅ / ✗ / ✓ (this repository's marker for a specimen). For the
rest, suppress a single line or a span:

    這行示範了禁用寫法  <!-- zhtw-lint: skip -->

    <!-- zhtw-lint: off -->
    ...text that must not be checked...
    <!-- zhtw-lint: on -->

Prefer `skip`: the block form is a standalone line, so putting it inside a list
or a blockquote splits the block and renumbers what follows. Ending a file
inside an `off` region is an error, so a stray marker cannot silently disable
the tail of a document.

The 簡體殘留 check is exact only when `opencc` is importable. Without it the
glyph table is derived from terms.csv and covers roughly 200 characters -- the
ones that show up in IT vocabulary. It reliably catches 数据/组件/服务器, and it
will miss fluent simplified prose built from 这/来/说/学/长/东 and the rest of the
everyday vocabulary the table never had a reason to contain. A clean run without
opencc means "no simplified IT terms", not "no simplified text". Install
`opencc` (see scripts/requirements.txt) to make it exhaustive.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

TERMS = Path(__file__).resolve().parent.parent / "references" / "terms.csv"
GLOSSARY_TYPE = "glossary"

CJK = r"一-鿿"
CJK_RE = re.compile(f"[{CJK}]")
DASH = "——"

# Half-width marks that a CJK sentence should not contain. Both sides matter:
# the mark must follow a CJK character, and be followed by whitespace, the end
# of the line, or another CJK character. That last case is the common one --
# 「中文,中文」 has no space anywhere -- while keeping "Button.tsx", "3.14" and
# "README.md" out, since their punctuation sits between ASCII.
HALFWIDTH_RE = re.compile(f"[{CJK}]([,;:!?.])(?=\\s|$|[{CJK}])")

BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
# A full stop inside a bold span means a whole sentence was bolded. Commas and
# 、 also occur in bolded pseudo-headings, so they are not evidence.
BOLD_SENTENCE_RE = re.compile(r"[。？！]")

LINT_OFF = re.compile(r"<!--\s*zhtw-lint:\s*off\s*-->")
LINT_ON = re.compile(r"<!--\s*zhtw-lint:\s*on\s*-->")
LINT_SKIP = re.compile(r"<!--\s*zhtw-lint:\s*skip\s*-->")

# Lines a ❌/✅ pair marks as a specimen. A style guide cannot demonstrate the
# thing it forbids without writing it down once, and the marker is already the
# repository's convention for "this is the wrong version".
SPECIMEN_RE = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+|>\s*)*[❌✅✓✗]")


class Finding:
    def __init__(self, path: str, line: int, check: str, message: str):
        self.path, self.line, self.check, self.message = path, line, check, message

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: [{self.check}] {self.message}"


# --- masking -----------------------------------------------------------------


def mask(lines: list[str]) -> tuple[list[str], list[bool]]:
    """Blank out regions no check should see; return (masked lines, checkable).

    Masked rather than deleted so line numbers stay usable in the report.
    """
    out: list[str] = []
    live: list[bool] = []
    fence: str | None = None
    in_front = False
    suppressed = False

    for i, raw in enumerate(lines):
        stripped = raw.strip()

        if i == 0 and stripped == "---":
            in_front = True
            out.append("")
            live.append(False)
            continue
        if in_front:
            if stripped == "---":
                in_front = False
            out.append("")
            live.append(False)
            continue

        # Track which marker opened the block. A single boolean lets a ~~~ line
        # inside a ``` block close it, exposing genuine code to the checks.
        if fence is None and (stripped.startswith("```") or stripped.startswith("~~~")):
            fence = stripped[:3]
            out.append("")
            live.append(False)
            continue
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            out.append("")
            live.append(False)
            continue

        if LINT_OFF.search(raw):
            suppressed = True
            out.append("")
            live.append(False)
            continue
        if LINT_ON.search(raw):
            suppressed = False
            out.append("")
            live.append(False)
            continue
        if suppressed:
            out.append("")
            live.append(False)
            continue

        # Table rows carry the ban tables and their arrows; a cell is a label,
        # not a sentence, so punctuation and bold rules do not apply.
        if stripped.startswith("|"):
            out.append("")
            live.append(False)
            continue

        if LINT_SKIP.search(raw) or SPECIMEN_RE.match(stripped):
            out.append("")
            live.append(False)
            continue

        text = re.sub(r"`[^`]*`", " ", raw)          # inline code
        text = re.sub(r"\]\([^)]*\)", "] ", text)     # link targets
        text = re.sub(r"https?://\S+", " ", text)
        out.append(text)
        live.append(True)

    if suppressed:
        raise ValueError("file ends inside a `zhtw-lint: off` region")
    if fence is not None:
        # Same reasoning as the unclosed `off` region: an unterminated fence
        # masks everything after it, and a silent pass looks like a clean file.
        raise ValueError(f"file ends inside an unclosed `{fence}` code fence")
    return out, live


# --- checks ------------------------------------------------------------------


def check_halfwidth(path: str, masked: list[str]) -> list[Finding]:
    found = []
    for n, line in enumerate(masked, 1):
        for m in HALFWIDTH_RE.finditer(line):
            mark = m.group(1)
            found.append(
                Finding(path, n, "半形標點", f"中文句子用了半形「{mark}」：…{line[max(0, m.start()):m.end() + 12].strip()}…")
            )
    return found


def check_dash_density(path: str, masked: list[str]) -> list[Finding]:
    text = "\n".join(masked)
    cjk = len(CJK_RE.findall(text))
    if not cjk:
        return []
    used = text.count(DASH)
    cap = max(1, cjk // 1000)
    if used <= cap:
        return []
    lines = [n for n, line in enumerate(masked, 1) if DASH in line]
    return [
        Finding(
            path,
            lines[cap] if len(lines) > cap else lines[-1],
            "破折號密度",
            f"{used} 組 / {cjk} 中文字，上限 {cap} 組（出現在 L{', L'.join(map(str, lines))}）",
        )
    ]


def check_bold(path: str, masked: list[str]) -> list[Finding]:
    """One bold span per paragraph; never a whole bolded sentence.

    A list item is its own paragraph. A bullet list where every item opens with
    a bolded term (`- **快取**：…`) is a definition list, the single most common
    shape in these documents; folding the whole list into one paragraph reports
    it as an eight-fold violation every time.
    """
    found = []
    para: list[tuple[int, str]] = []

    def flush() -> None:
        if not para:
            return
        spans = [(n, s) for n, line in para for s in BOLD_RE.findall(line)]
        # A bolded lead-in is the label of a definition entry, not one of the
        # paragraph's emphasis marks. `- **prose-style.md**：只在…時讀，其他**不要讀**`
        # spends its one allowance on 不要讀; charging the label as well would
        # make every definition list unfixable without dropping the labels.
        first = para[0][1].strip()
        lead = re.match(r"(?:[-*+]\s+|\d+[.)]\s+)?\*\*(.+?)\*\*", first)
        counted = spans[1:] if (lead and spans and spans[0][1] == lead.group(1)) else spans
        if len(counted) > 1:
            found.append(
                Finding(
                    path,
                    counted[1][0],
                    "加粗密度",
                    f"同一段有 {len(counted)} 處加粗，上限 1 處：{'、'.join(s for _, s in counted[:3])}",
                )
            )
        # The whole-sentence rule applies to every span, lead-in included: a
        # bolded label is fine, a bolded sentence standing in for one is not.
        for n, s in spans:
            # 「，」and 「、」appear inside ordinary emphasis and inside bolded
            # pseudo-headings alike; a full stop is what makes it a sentence.
            if BOLD_SENTENCE_RE.search(s):
                found.append(Finding(path, n, "整句加粗", f"加粗跨越整句：{s[:40]}"))
        para.clear()

    for n, line in enumerate(masked, 1):
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        if re.match(r"[-*+]\s|\d+[.)]\s|#{1,6}\s", stripped):
            flush()
        para.append((n, line))
    flush()
    return found


# Traditional characters that only ever occur on the mainland side of terms.csv
# (清晰度→解析度, 短信→簡訊, 触碰→輕觸), so no tw value vouches for them and the
# fallback would report them as simplified.
#
# Not collected one bug report at a time: this is the complete set for the
# current terms.csv, obtained by running the fallback with an opencc oracle and
# subtracting the glyphs opencc calls simplified. Regenerate after regrowing
# terms.csv with scripts/audit_shared_glyphs.py. Install opencc to make the
# whole list unnecessary.
SHARED_GLYPHS = set("崩捆晰短碰")


def load_simplified_only() -> set[str]:
    """The set of simplified-only glyphs, exactly if opencc is installed.

    With opencc a character is simplified iff converting it to traditional
    changes it. That is the real definition and needs no table.

    Without it, fall back to terms.csv: glyphs that appear in a *glossary* cn
    value and nowhere traditional. Only glossary rows feed the candidate set --
    the ruleset rows store their cn column in traditional glyphs (封禁, 疑難解答,
    市場細分), so counting them as evidence of simplification marks 禁, 答 and 細
    as simplified and floods every document with false positives.

    The fallback leaks both ways. False positives are fixable and fixed:
    SHARED_GLYPHS holds every traditional character the derivation currently
    misreads, audited against opencc rather than collected as they surface.
    Misses are not fixable -- a simplified character that never reaches a
    glossary cn value has no evidence to be derived from (织), and the resulting
    ~200 glyphs are all IT vocabulary, so fluent simplified prose passes.

    Only the tw and ruleset-cn columns count as evidence. note and clues are
    free prose that quote both scripts; harvesting them would vouch for 数, 件,
    步, 服, 器, 函, 量 and 存, gutting the check to buy nothing (the shared
    glyphs it would clear, such as 碰, do not appear there anyway).

    Treat a clean fallback run as "no obvious simplified text", not as proof.
    """
    try:
        import opencc  # type: ignore

        converter = opencc.OpenCC("s2t")
        return {chr(c) for c in range(0x4E00, 0x9FFF) if converter.convert(chr(c)) != chr(c)}
    except Exception:
        pass

    if not TERMS.exists():
        return set()
    candidates: set[str] = set()
    traditional: set[str] = set()
    with TERMS.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("type") == GLOSSARY_TYPE:
                candidates.update(CJK_RE.findall(row.get("cn", "") or ""))
            else:
                traditional.update(CJK_RE.findall(row.get("cn", "") or ""))
            traditional.update(CJK_RE.findall(row.get("tw", "") or ""))
    return candidates - traditional - SHARED_GLYPHS


def simplified_is_exact() -> bool:
    try:
        import opencc  # noqa: F401  # type: ignore

        return True
    except Exception:
        return False


def check_simplified(path: str, masked: list[str], simplified: set[str]) -> list[Finding]:
    found = []
    for n, line in enumerate(masked, 1):
        hits = sorted({ch for ch in line if ch in simplified})
        if hits:
            found.append(Finding(path, n, "簡體殘留", f"出現簡體字 {'、'.join(hits)}：{line.strip()[:50]}"))
    return found


def load_terms() -> list[tuple[str, str, list[str], list[str]]]:
    """(cn, tw, clues, avoid_clues) for multi-character entries.

    Single characters are skipped: they match inside unrelated words far more
    often than they catch a real one.
    """
    rows = []
    with TERMS.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cn, tw = row["cn"], row["tw"]
            if len(cn) < 2 or not tw or row["type"] == "disabled":
                continue
            # 34 glossary rows carry the same string on both sides (容器, 下拉,
            # 框架): the term is simply shared. Reporting them yields 「下拉 →
            # 下拉」, which trains the reader to ignore the whole check.
            if cn == tw:
                continue
            rows.append(
                (cn, tw, [c for c in row["clues"].split("；") if c], [c for c in row["avoid_clues"].split("；") if c])
            )
    return rows


def check_terms(path: str, masked: list[str], terms) -> list[Finding]:
    found = []
    for n, line in enumerate(masked, 1):
        for cn, tw, clues, avoid in terms:
            if cn not in line:
                continue
            if any(a in line for a in avoid):
                continue
            confidence = "" if not clues else ("" if any(c in line for c in clues) else "（語境未確認）")
            found.append(Finding(path, n, "用詞", f"{cn} → {tw}{confidence}"))
    return found


# --- driver ------------------------------------------------------------------


def lint(path: Path, terms) -> list[Finding]:
    try:
        lines = path.read_text(encoding="utf-8").split("\n")
    except UnicodeDecodeError as exc:
        return [Finding(str(path), 1, "讀取失敗", f"不是 UTF-8：{exc}")]
    try:
        masked, _ = mask(lines)
    except ValueError as exc:
        return [Finding(str(path), len(lines), "標記錯誤", str(exc))]

    simplified = load_simplified_only()
    found = (
        check_halfwidth(str(path), masked)
        + check_dash_density(str(path), masked)
        + check_bold(str(path), masked)
        + check_simplified(str(path), masked, simplified)
    )
    if terms is not None:
        found += check_terms(str(path), masked, terms)
    return sorted(found, key=lambda f: (f.line, f.check))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument(
        "--terms",
        action="store_true",
        help="also check vocabulary against references/terms.csv (noisy on documents that quote banned words)",
    )
    args = parser.parse_args()

    terms = load_terms() if args.terms else None
    if not simplified_is_exact():
        print(
            f"note: opencc not installed -- 簡體殘留 covers only the "
            f"{len(load_simplified_only())} glyphs derivable from terms.csv. It catches "
            "simplified IT terms; fluent simplified prose can still pass.",
            file=sys.stderr,
        )
    total = 0
    for path in args.paths:
        if not path.is_file():
            print(f"{path}: not a file", file=sys.stderr)
            return 2
        for finding in lint(path, terms):
            print(finding)
            total += 1

    print(f"\n{total} finding(s) in {len(args.paths)} file(s)", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
