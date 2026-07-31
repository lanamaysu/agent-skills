# Reference Files

本資料夾包含技能參考資料。維護工具在 `../scripts/`。

## Files

### guidelines.md

**完整技術寫作指南**：包含所有規範與範例

- 核心術語對照（常用 + 領域）
- 保留英文的技術術語清單，含英文命名禁止無意義音譯
- 標點符號與格式規則
- 實務範例（程式碼、commit、錯誤訊息）
- 中國用語過濾：表外詞彙與非 IT 領域，含「怎麼 grep terms.csv」

**使用時機**：品質檢查未通過，或使用者明確要求術語稽核時讀取。

### prose-style.md

**去 AI 味的行文規範**：限用與禁用清單、正向原則、產出前自我檢查。

**使用時機**：只在寫連續中文散文時讀（專案文件、README 敘述段落、ADR、release note、規格書、簡報）。commit message、程式碼註解、測試案例描述、表格與 API 參數說明不要讀，那些是固定格式，套散文的節奏規範會把格式帶壞；`SKILL.md` 的「AI 味速查」那層已經涵蓋。

**來源**：改寫自 [allenloves/de-ai-tone](https://github.com/allenloves/de-ai-tone)，授權 CC BY-SA 4.0，刪去翻譯與音樂領域規則，例句改為軟體開發情境。本檔同樣以 CC BY-SA 4.0 釋出。

### terms.csv

**來源**：[大陸台灣計算機術語對照表（Wikibooks）](https://zh.wikibooks.org/zh-tw/%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8)
**授權**：創用 CC BY-SA 4.0（需標示來源並以相同方式分享）

**授權標示範例**：

- 來源：Wikibooks《大陸台灣計算機術語對照表》
- 授權：CC BY-SA 4.0
- 連結：https://creativecommons.org/licenses/by-sa/4.0/

**欄位**（依序，第一欄是英文）：

| 欄 | 內容 |
|----|------|
| `en` | 英文原文 |
| `tw` | 台灣繁體中文術語 |
| `cn` | 中國大陸簡體中文術語 |

**統計**：

- 資料列：464（含標題共 465 行）
- 大小：18 KB
- 格式：CSV（UTF-8）、LF 換行

**用 grep 查，不要整份讀。** 整份讀進 context 要 4,000-6,000 token，只為換幾行結果。

```bash
# 依英文術語查
grep -i "array" terms.csv

# 依台灣術語查
grep "陣列" terms.csv

# cn 欄存的是簡體字形。可疑詞是繁體時（「數據」），要 grep 它的簡體形
grep -n '数据\|组件\|视频' terms.csv
```

**多義詞**：同一個英文詞若有兩個義項，會出現兩列。`Comment (code)`、`Flush (align)`、`Token (security/currency)` 這三個義項標註是手動加的，重新抓取會蓋掉，先 diff 再覆蓋。

**更新**：見 `../scripts/`。

---

**最後更新**：2026-07-31
