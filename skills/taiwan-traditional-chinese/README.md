# Taiwan Traditional Chinese Skill

台灣繁體中文寫作規範：術語、標點、去 AI 味。`SKILL.md` 為技能入口。

## 適用範圍

判準是**產出物的語言，不是關鍵字**：只要你要產出的東西含中文，就適用。

- commit message、PR 描述、ADR、規格書、README、專案文件、簡報
- 程式碼註解、測試案例描述、UI 文案、`zh-TW` locale 檔
- 使用者用中文提問，或說「用中文」時的一般回覆
- 修既有中文：中國用語、軟體圈行話（落地／對齊／閉環）、台灣術語、AI 味

不適用：中文只是 bug 的主體（字型 fallback、編碼、全形空白、繁簡轉換套件），或翻譯成非中文語言。

## 安裝

```bash
npx skills add lanamaysu/agent-skills --skill taiwan-traditional-chinese
```

或列出所有可用技能：

```bash
npx skills add lanamaysu/agent-skills --list
```

## 使用重點

`SKILL.md` 內含四張常時生效的表，產出前掃一遍就能第一次寫對：

| 表 | 管什麼 |
|----|--------|
| 關鍵術語速查表 | 20 組必用台灣術語 + 絕對禁用清單 |
| 中國軟體圈行話禁用表 | 落地、復盤、閉環、抓手、顆粒度⋯⋯ |
| 一詞多義 | 質量、水平、通過、項目、對齊、數據 —— 看義項判斷，不是全面禁用 |
| AI 味速查 | 空轉話語標記、貼標語彙、破折號與排比的量化上限、開場收場 |

references 預設不讀，只在品質檢查未通過或明確要求稽核時才進 context：

- `references/prose-style.md` — 寫連續散文時讀
- `references/guidelines.md` — 稽核時讀
- `references/terms.csv` — **永遠用 `grep` 查，不要整份讀**

### 通用規則

- 使用者說「用中文／中文回答／中文輸出」，預設視為繁體中文（台灣）
- 檔案路徑與程式碼用反引號標示，不要做成連結
- 中文句子用全形標點，程式碼與路徑用半形標點
- 框架名稱、API、程式碼符號保留英文
- 禁用詞包含：組件、異步、數據、服務器、函數、數組等

## 授權與資料來源

- `references/terms.csv` 來源有二：Wikibooks《大陸台灣計算機術語對照表》（CC BY-SA 4.0，同方式分享）；[sysprog21/zhtw-mcp](https://github.com/sysprog21/zhtw-mcp) 的 `assets/ruleset.json`（MIT，跨海峽詞條再上溯 [OpenCC](https://github.com/BYVoid/OpenCC)，Apache-2.0）。
- `references/prose-style.md`、`SKILL.md` 的軟體圈行話表與一詞多義表：改寫自 [allenloves/de-ai-tone](https://github.com/allenloves/de-ai-tone)，授權 CC BY-SA 4.0，同方式分享。
- 若再散佈此技能，請保留來源與授權連結：https://creativecommons.org/licenses/by-sa/4.0/

## 維護者：更新對照表（選用）

一般使用者無需執行此步驟。僅供維護者更新術語表時使用。

```bash
# 建立/啟用虛擬環境（若尚未建立）
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt

# 兩個來源都重抓並產生 references/terms.csv
.venv/bin/python scripts/fetch_terms.py

# 只更新 zhtw-mcp 規則（純標準函式庫，不需要 venv）
python3 scripts/fetch_terms.py --source ruleset

# 只重抓 Wikibooks
.venv/bin/python scripts/fetch_terms.py --source glossary
```

重新抓取 glossary 會蓋掉手動加的義項標註（`Comment (code)`、`Flush (align)`、`Token (security/currency)`）與 `Token` 的 `cn` 欄修正，**先 diff 再覆蓋**。腳本會處理 Wikibooks 表格的 `rowspan` 合併儲存格；若 `en` 欄出現非 ASCII 就會中止而不覆寫，那代表上游表格結構變了。`--source` 只重抓一邊，另一邊沿用檔案裡既有的列，所以 Wikibooks 這半邊掛掉時不會連帶影響規則更新。

## 數量類檢查（選用）

`SKILL.md` 的四張表管用詞與語氣，模型讀得到、也判得準。判不準的是要數數字的那幾條，`scripts/lint_zhtw.py` 只補這一塊：

```bash
python3 scripts/lint_zhtw.py <file.md>...      # 半形標點、破折號密度、加粗密度、整句加粗、簡體殘留
python3 scripts/lint_zhtw.py --terms <file.md> # 另外比對 terms.csv 的用詞（會吵，只在稽核時開）
python3 scripts/test_lint_zhtw.py              # fixture 測試，每條檢查都有正反例
```

不進技能的載入路徑，context 成本為零。程式碼區塊、行內程式碼、表格列、YAML frontmatter 與 `❌`／`✅` 開頭的示範行都會自動略過；其餘要豁免的地方用行尾 `<!-- zhtw-lint: skip -->`。

`簡體殘留` 只有裝了 `opencc` 才完整。沒裝時字表從 `terms.csv` 推出來，只有 201 字，涵蓋 IT 詞彙：抓得到 `数据`、`组件`、`服务器`，抓不到用 `这`、`来`、`说`、`学`、`东` 寫成的日常簡體散文。沒命中只代表「沒有簡體 IT 用語」，不代表「沒有簡體」。

推導出來的字表另有一批誤報：只出現在對照表中國側的繁體字（`触碰` 的「碰」、`清晰度` 的「晰」）沒有任何台灣側詞條可以為它背書，會被當成簡體。這批已經清乾淨，做法不是等它被踩到才補，而是用 `opencc` 當對照跑一次差集：

```bash
.venv/bin/python scripts/audit_shared_glyphs.py   # 重新產 terms.csv 後跑
```

腳本會印出正確的字表並在與 `lint_zhtw.py` 不一致時回傳 1。

`--terms` 跟 `SKILL.md` 的禁用表確實有重疊，這是刻意的分工：表在 context 裡負責產出時寫對，`--terms` 讀 `terms.csv` 負責事後稽核既有檔案，兩邊都不複製詞表。代價是它很吵（本專案 7 份文件會出 85 筆，多數是文件在講這些詞本身），所以預設關閉。

## 結構

- `SKILL.md` — 技能入口：四張常時生效的表 + 品質檢查流程
- `references/` — 按需載入的參考資料
  - `prose-style.md` — 去 AI 味的完整行文規範（寫散文時讀）
  - `guidelines.md` — 完整技術寫作指南（稽核時讀）
  - `terms.csv` — 術語對照表 2,122 筆，欄位 `en,tw,cn,type,clues,avoid_clues,note`（用 `grep` 查）
  - `README.md` — 資料來源、授權與欄位說明
- `scripts/` — 維護工具
  - `fetch_terms.py` — 從 Wikibooks 與 zhtw-mcp ruleset 抓取並合併輸出 CSV
  - `lint_zhtw.py` — Markdown 的數量類檢查（見下）
  - `test_lint_zhtw.py` — lint 的 fixture 測試
  - `audit_shared_glyphs.py` — 用 `opencc` 校正 lint 的簡體字表（需要 opencc）
  - `requirements.txt` — 抓取腳本的相依性

---

**Last Updated**: 2026-08-09
