# taiwan-traditional-chinese bench

比較「沒有 skill」與「有 skill」兩個 arm，測三件事：術語、語氣、整體文字品質。

## 執行

```bash
cd <repo 根目錄>

./bench/run.sh                    # 六次呼叫，約十分鐘
python3 bench/score.py      bench/out-terms-none.txt bench/out-terms-new.txt
python3 bench/tone_score.py bench/out-tone-none.txt  bench/out-tone-new.txt
python3 bench/blind.py            # 生成題盲測，產生 blind.md
```

只跑其中一組：`./bench/run.sh default terms`（可選 `terms` / `gen` / `tone` / `all`）。

換模型：`./bench/run.sh haiku`，輸出檔前綴會變成 `haiku-`，計分指令跟著換檔名。
盲測看別組結果用 `BENCH_PREFIX=haiku python3 bench/blind.py`。

## 盲測怎麼做

`blind.py` 把兩個 arm 的生成題輸出打散成 A／B，順序每題重洗。

1. 打開 `bench/blind.md`，每題挑一個你最想直接拿去用的版本。
2. **不要開 `blind-key.txt`。**
3. 選完跑 `python3 bench/blind.py G1=A G2=B G3=A`，它會告訴你選到誰。

## 三組題目

| 組別 | 題數 | 題目來源 | 計分 |
|---|---|---|---|
| 術語 | 12 | `items.csv` | `score.py`：只看目標詞，`banned` 不能出現、`required` 要中一個 |
| 語氣 | 3 篇長文 | `prompt-tone.md` | `tone_score.py`：數違規／千字 |
| 生成 | 3 篇短文 | `prompt-gen.md` | `blind.py`：人工盲選 |

術語題分三層：常見詞 1（代碼→程式碼，預期平手）、冷僻詞 7（查表才會）、防守題 4（看起來像中國用語、其實是台灣正確用法，改了就扣分）。防守題讓「全部改」和「全部不改」兩種投機解都拿不到分。

改題目只要動 `items.csv`，然後跑 `python3 bench/gen_prompts.py` 重新生成 `prompt.md` 和 `prompt-baseline-neutral.md`，那兩份不要手改。

`required` 只放能區分中國用語與台灣用語的最短字串，不要放整個詞。O6 的 `required` 是「配置」不是「頁面配置」，因為 baseline 寫過「分頁配置」——換說法不是中國用語，判 MISS 等於在罰改寫。

## 已知限制，報告要一起寫

1. **語氣計分是循環的。** `tone_score.py` 的清單來自 SKILL.md 和 prose-style.md，拿 skill 自己的規則評 skill 的產出，對 skill 有利。可信之處在於清單公開可逐條核對，但不能宣稱中立。
2. **字數要跟違規數一起看。** 內容砍光違規也會歸零，所以 `tone_score.py` 一定把中文字數印在旁邊。
3. **baseline 不是完全乾淨的。** `--disallowed-tools Skill Read Grep Glob` 擋掉了 skill 呼叫，但系統提示裡仍有各 skill 的 description 和 user CLAUDE.md。改 `CLAUDE_CONFIG_DIR` 可以隔離，代價是連憑證一起隔離掉、變成未登入，所以沒有這樣做。
4. **每個 arm 只跑一次。** 單次呼叫會 flake（v1 有一次生成題回傳空檔），n=12 題加 3 篇長文只夠說「示範」，不夠說「統計顯著」。
5. **haiku 的 skill arm 術語分數波動極大，只能寫區間。** 四次分別是 10/12、2/12、12/12、6/12。追工具軌跡看出分水嶺是 `lint_zhtw.py` 有沒有真的跑起來：模型第一直覺是 `--terms -` 走 stdin，腳本原本不吃 stdin，報錯之後有時改用暫存檔重試（拿到 12/12），有時就放棄查表直接輸出（2/12）。腳本已補上 stdin、SKILL.md 也改成示範 heredoc，**補完之後那次是 6/12，波動沒有收斂**——輸出裡「宏內核」「情景模式」原封不動，兩個都是 terms.csv 精確命中、腳本一定會報的詞，所以是腳本沒跑或跑了沒理。

   對照組穩定得多（haiku baseline 三次 5、6、6），所以不穩的是 skill arm 的多步工具流程，不是題目。報告寫 haiku 術語只能寫「2 到 12 分之間」，寫單一數字都是在挑資料。

6. **語氣結論兩個模型同向，術語結論不是。** 語氣：預設模型 3.0 → 0.0／千字，haiku 7.0 → 0.0／千字，字數沒掉（haiku skill arm 721 字 vs baseline 718 字）。術語：預設模型 9/12 → 12/12 可信，haiku 不穩。可以主張的是「語氣規則對任何模型都有效，術語查表需要能穩定跑完多步工具流程的模型」。

## 目錄

- `RESULTS.md` — 實測結果，要給人看的就是這份
- `items.csv` — 術語題與標準答案
- `prompt*.md` — 六份提示，`*-neutral.md` 是 baseline 用的；`prompt.md` 與 `prompt-baseline-neutral.md` 由 `gen_prompts.py` 生成，不要手改
- `run.sh` — 跑兩個 arm
- `gen_prompts.py` — 從 `items.csv` 生成術語題的兩份提示
- `score.py` / `tone_score.py` / `blind.py` — 三種計分
- `results-2026-08-10/` — RESULTS.md 引用的那次執行的原始輸出，凍結不動
- `items-v1.csv` / `v1-results/` — 被取代的第一版題目與結果，只留作對照

執行產生的 `out-*.txt`、`haiku-*.txt`、`blind.md`、`blind-key.txt` 都在 `.gitignore` 裡，每次跑都會覆寫。要保存某次結果就複製到 `results-<日期>/`。
