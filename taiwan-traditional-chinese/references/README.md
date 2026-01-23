# Reference Files

本資料夾包含技能檔案參考的外部資源。

## Files

### terms.csv

**來源**: [大陸台灣計算機術語對照表（Wikibooks）](https://zh.wikibooks.org/zh-tw/%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8)
**授權**: 創用 CC BY-SA 4.0（需標示來源並以相同方式分享）

**授權標示範例**:
- 來源：Wikibooks《大陸台灣計算機術語對照表》
- 授權：CC BY-SA 4.0
- 連結：https://creativecommons.org/licenses/by-sa/4.0/

**說明**: 包含超過 1600 個技術術語的台灣繁體中文 vs Mainland 簡體中文對照表。

**欄位**:

- Column 1: 台灣繁體中文術語
- Column 2: Mainland 簡體中文術語
- Column 3: 英文原文

**統計**:

- 行數: 1,632
- 大小: 86KB
- 格式: CSV (UTF-8)

**用途**:

- 查詢正確的台灣技術術語
- 確認 Mainland 術語的對應
- 建立術語標準化指南

**範例查詢**:

```bash
# 搜尋特定英文術語
grep -i "array" terms.csv

# 搜尋台灣術語
grep "陣列" terms.csv

# 統計術語數量
wc -l terms.csv
```

**更新**:
- 使用腳本重新抓取：`.venv/bin/python references/fetch_terms.py`
- 若未建立虛擬環境，可先執行：`python3 -m venv .venv && .venv/bin/pip install pandas lxml requests beautifulsoup4`

---

**最後更新**: 2026-01-23
