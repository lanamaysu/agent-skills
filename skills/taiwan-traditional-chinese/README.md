# Taiwan Traditional Chinese Skill

可用 `npx add-skill <repo-url>` 安裝；技能入口檔案為 `SKILL.md`。

## 授權與資料來源
- `references/terms.csv` 來源：Wikibooks《大陸台灣計算機術語對照表》，授權：CC BY-SA 4.0，同方式分享。
- 若再散佈此技能，請保留來源與授權連結：https://creativecommons.org/licenses/by-sa/4.0/

## 更新對照表
```bash
# 建立/啟用虛擬環境（若尚未建立）
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# 重新抓取 Wikibooks 對照表並產生 references/terms.csv
.venv/bin/python references/fetch_terms.py
```

## 結構
- SKILL.md — 技能說明、使用時機、步驟、疑難排解
- references/terms.csv — 術語對照表（由 fetch_terms.py 產出）
- references/fetch_terms.py — 從 Wikibooks 抓取表格並輸出 CSV
- references/README.md — 資料來源、授權與更新說明
- requirements.txt — 抓取腳本的依賴
