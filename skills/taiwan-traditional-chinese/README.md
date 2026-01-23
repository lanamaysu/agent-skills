# Taiwan Traditional Chinese Skill

台灣繁體中文回應指南。SKILL.md 為技能入口。

## 安裝

```bash
npx add-skill lanamaysu/agent-skills --skill taiwan-traditional-chinese
```

或列出所有可用技能：

```bash
npx add-skill lanamaysu/agent-skills --list
```

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
- SKILL.md — 技能說明、使用時機、步驟、疑難排解
- references/ — 參考資料與維護工具
  - terms.csv — 術語對照表（由 fetch_terms.py 產出）
  - fetch_terms.py — 從 Wikibooks 抓取表格並輸出 CSV
  - requirements.txt — 抓取腳本的依賴
  - README.md — 資料來源、授權與更新說明
