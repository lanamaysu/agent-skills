# Taiwan Traditional Chinese Skill

台灣繁體中文回應指南。`SKILL.md` 為技能入口。

## 適用範圍

- 使用者要求中文或繁體中文輸出時。
- 撰寫回應、註解、文件、在地化文案時。
- 需要台灣術語、標點與語氣一致性時。

## 安裝

```bash
npx add-skill lanamaysu/agent-skills --skill taiwan-traditional-chinese
```

或列出所有可用技能：

```bash
npx add-skill lanamaysu/agent-skills --list
```

## 使用重點

### 針對不同模型的優化

**小模型（Claude Haiku, GPT-4o mini）**：
- SKILL.md 內建**關鍵術語速查表**，包含 20+ 最常用台灣術語
- 無需品質檢查流程，直接參考速查表產出正確輸出
- 只有使用者明確要求術語稽核時，才讀取完整參考文件

**大模型（Claude Sonnet/Opus, GPT-4）**：
- 先產出草稿並自我檢查
- 未通過時才讀取 `references/guidelines.md` 與 `references/terms.csv`
- 可處理更複雜的術語稽核任務

### 通用規則

- 若使用者說「用中文／中文回答／中文輸出」，預設視為繁體中文（台灣）
- 檔案路徑與程式碼請使用反引號標示
- 禁用詞包含：組件、異步、數據、服務器、函數、數組等

## 授權與資料來源

- `references/terms.csv` 來源：Wikibooks《大陸台灣計算機術語對照表》，授權：CC BY-SA 4.0，同方式分享。
- 若再散佈此技能，請保留來源與授權連結：https://creativecommons.org/licenses/by-sa/4.0/

## 維護者：更新對照表（選用）

一般使用者無需執行此步驟。僅供維護者更新術語表時使用。

```bash
# 建立/啟用虛擬環境（若尚未建立）
python3 -m venv .venv && .venv/bin/pip install -r references/requirements.txt

# 重新抓取 Wikibooks 對照表並產生 references/terms.csv
.venv/bin/python references/fetch_terms.py
```

## 結構

- `SKILL.md` — 技能說明、使用時機、步驟、疑難排解
- `references/` — 參考資料與維護工具
  - `terms.csv` — 術語對照表（由 `fetch_terms.py` 產出）
  - `fetch_terms.py` — 從 Wikibooks 抓取表格並輸出 CSV
  - `requirements.txt` — 抓取腳本的相依性
  - `README.md` — 資料來源、授權與更新說明
