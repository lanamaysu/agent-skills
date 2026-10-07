"""Recompute SHARED_GLYPHS in lint_zhtw.py. Run after regenerating terms.csv.

    pip install opencc-python-reimplemented
    python3 scripts/audit_shared_glyphs.py

Without opencc the linter derives its simplified-glyph set from terms.csv, and
that derivation reports a handful of traditional characters that happen to sit
only on the mainland side of the table. This script names all of them at once
instead of waiting for each to surface as a false positive: build the derived
set with the patch list emptied, then subtract what opencc actually calls
simplified. Whatever is left is the patch list.

Prints the new value and exits 1 if it differs from the one in lint_zhtw.py.
"""
from __future__ import annotations

import csv
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TERMS = HERE.parent / "references" / "terms.csv"
CJK_RE = re.compile(r"[一-鿿]")

try:
    import opencc  # type: ignore
except ImportError:
    sys.exit("opencc not installed: pip install opencc-python-reimplemented")

spec = importlib.util.spec_from_file_location("lint_zhtw", HERE / "lint_zhtw.py")
lint_zhtw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint_zhtw)

converter = opencc.OpenCC("s2t")
simplified = {chr(c) for c in range(0x4E00, 0x9FFF) if converter.convert(chr(c)) != chr(c)}

candidates: set[str] = set()
traditional: set[str] = set()
with TERMS.open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("type") == lint_zhtw.GLOSSARY_TYPE:
            candidates.update(CJK_RE.findall(row.get("cn", "") or ""))
        else:
            traditional.update(CJK_RE.findall(row.get("cn", "") or ""))
        traditional.update(CJK_RE.findall(row.get("tw", "") or ""))

derived = candidates - traditional
audited = derived - simplified
current = lint_zhtw.SHARED_GLYPHS

print(f"derived set: {len(derived)} glyphs")
print(f"real simplified: {len(derived & simplified)}")
print(f"SHARED_GLYPHS should be: {''.join(sorted(audited))}")

if audited == current:
    print("lint_zhtw.py is up to date")
    sys.exit(0)

print(f"lint_zhtw.py currently has: {''.join(sorted(current))}")
print(f"  add:    {''.join(sorted(audited - current)) or '(none)'}")
print(f"  remove: {''.join(sorted(current - audited)) or '(none)'}")
sys.exit(1)
