# Taiwan Traditional Chinese Skill

台灣繁體中文寫作規範：術語、標點、去 AI 味。`SKILL.md` 為技能入口。

## 適用範圍

判準是**產出物的語言，不是關鍵字**：只要你要產出的東西含中文，就適用。

- commit message、PR 描述、ADR、規格書、README、專案文件、簡報
- 程式碼註解、測試案例描述、UI 文案、`zh-TW` locale 檔
- 使用者用中文提問，或說「用中文」時的一般回覆
- 修既有中文：中國用語、科技業套話（落地／對齊／閉環）、台灣術語、AI 味

不適用：中文只是 bug 的主體（字型 fallback、編碼、全形空白、繁簡轉換套件），或翻譯成非中文語言。

## 安裝

```bash
npx add-skill lanamaysu/agent-skills --skill taiwan-traditional-chinese
```

或列出所有可用技能：

```bash
npx add-skill lanamaysu/agent-skills --list
```

## 使用重點

`SKILL.md` 內含四張常時生效的表，產出前掃一遍就能第一次寫對：

| 表 | 管什麼 |
|----|--------|
| 關鍵術語速查表 | 20 組必用台灣術語 + 絕對禁用清單 |
| 中國科技業套話禁用表 | 落地、復盤、閉環、抓手、顆粒度⋯⋯ |
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

- `references/terms.csv` 來源：Wikibooks《大陸台灣計算機術語對照表》，授權 CC BY-SA 4.0，同方式分享。
- `references/prose-style.md`、`SKILL.md` 的科技業套話表與一詞多義表：改寫自 [allenloves/de-ai-tone](https://github.com/allenloves/de-ai-tone)，授權 CC BY-SA 4.0，同方式分享。
- 若再散佈此技能，請保留來源與授權連結：https://creativecommons.org/licenses/by-sa/4.0/

## 維護者：更新對照表（選用）

一般使用者無需執行此步驟。僅供維護者更新術語表時使用。

```bash
# 建立/啟用虛擬環境（若尚未建立）
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt

# 重新抓取 Wikibooks 對照表並產生 references/terms.csv
.venv/bin/python scripts/fetch_terms.py
```

重新抓取會蓋掉手動加的義項標註（`Comment (code)`、`Flush (align)`、`Token (security/currency)`）與 `Token` 的 `cn` 欄修正，**先 diff 再覆蓋**。腳本會處理 Wikibooks 表格的 `rowspan` 合併儲存格；若 `en` 欄出現非 ASCII 就會中止而不覆寫，那代表上游表格結構變了。

## 結構

- `SKILL.md` — 技能入口：四張常時生效的表 + 品質檢查流程
- `references/` — 按需載入的參考資料
  - `prose-style.md` — 去 AI 味的完整行文規範（寫散文時讀）
  - `guidelines.md` — 完整技術寫作指南（稽核時讀）
  - `terms.csv` — 術語對照表 464 筆，欄位 `en,tw,cn`（用 `grep` 查）
  - `README.md` — 資料來源、授權與欄位說明
- `scripts/` — 維護工具
  - `fetch_terms.py` — 從 Wikibooks 抓取表格並輸出 CSV
  - `requirements.txt` — 抓取腳本的相依性
