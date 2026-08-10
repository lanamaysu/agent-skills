#!/bin/bash
# 兩個 arm：none（沒有 skill）／new（有 skill，HEAD）
#
#   ./bench/run.sh            # 用預設模型
#   ./bench/run.sh haiku      # 指定 haiku
#   ./bench/run.sh haiku tone # 只跑語氣題（terms／gen／tone／all，預設 all）
#
# 沒有改 CLAUDE_CONFIG_DIR：那會連憑證一起隔離掉，變成未登入。
# 代價是 baseline 的系統提示仍看得到各 skill 的 description 和 user CLAUDE.md，
# 這點要寫進報告，不能當作沒有。
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)

TAG=${1:-default}
WHAT=${2:-all}

# bash 3.2（macOS 內建）在 set -u 下展開空陣列會報 unbound，
# 所以下面一律用 ${arr[@]+"${arr[@]}"} 這種寫法。
MODEL_ARGS=()
case "$TAG" in
  haiku)   MODEL_ARGS=(--model claude-haiku-4-5-20251001) ;;
  default) ;;
  *)       MODEL_ARGS=(--model "$TAG") ;;
esac
PREFIX=$([[ $TAG == default ]] && echo "out" || echo "$TAG")

# skill arm 需要 Bash：SKILL.md 第 2 步要跑 lint_zhtw.py 做機械比對。
# 沒有 Bash 就只能退回自己挑候選詞，而那正是弱模型查不到東西的原因。
SKILL_TOOLS=(--allowed-tools Read Grep Glob Bash Write)
# baseline 連檔案工具一起關，skill 才真的碰不到
NONE_TOOLS=(--disallowed-tools Skill Read Grep Glob)

run () {  # run <提示檔> <輸出檔> <旗標...>
  local prompt=$1 out=$2; shift 2
  echo "  -> $out"
  claude -p "$(cat "$ROOT/bench/$prompt")" ${MODEL_ARGS[@]+"${MODEL_ARGS[@]}"} "$@" > "$ROOT/bench/$out"
}

if [[ $WHAT == all || $WHAT == terms ]]; then
  echo "== 術語題（${TAG}）=="
  run prompt-baseline-neutral.md "$PREFIX-terms-none.txt" "${NONE_TOOLS[@]}"
  run prompt.md                  "$PREFIX-terms-new.txt"  "${SKILL_TOOLS[@]}"
fi

if [[ $WHAT == all || $WHAT == gen ]]; then
  echo "== 生成題（${TAG}）=="
  run prompt-gen-neutral.md "$PREFIX-gen-none.txt" "${NONE_TOOLS[@]}"
  run prompt-gen.md         "$PREFIX-gen-new.txt"  "${SKILL_TOOLS[@]}"
fi

if [[ $WHAT == all || $WHAT == tone ]]; then
  echo "== 語氣題（${TAG}）=="
  run prompt-tone-neutral.md "$PREFIX-tone-none.txt" "${NONE_TOOLS[@]}"
  run prompt-tone.md         "$PREFIX-tone-new.txt"  "${SKILL_TOOLS[@]}"
fi

echo
echo "python3 bench/score.py bench/$PREFIX-terms-none.txt bench/$PREFIX-terms-new.txt"
echo "python3 bench/tone_score.py bench/$PREFIX-tone-none.txt bench/$PREFIX-tone-new.txt"
