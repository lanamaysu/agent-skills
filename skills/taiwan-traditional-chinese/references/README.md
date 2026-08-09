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

**來源**：兩份資料合併，用 `type` 欄區分。

| `type` | 來源 | 授權 | `cn` 欄字形 |
|--------|------|------|-------------|
| `glossary` | [大陸台灣計算機術語對照表（Wikibooks）](https://zh.wikibooks.org/zh-tw/%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8) | CC BY-SA 4.0 | 簡體 |
| `cross_strait`、`variant`、`confusable`、`political_coloring`、`disabled` | [sysprog21/zhtw-mcp](https://github.com/sysprog21/zhtw-mcp) `assets/ruleset.json` | MIT（跨海峽詞條再上溯 [OpenCC](https://github.com/BYVoid/OpenCC)，Apache-2.0） | 繁體 |

兩種字形都留著是刻意的：grep「數據」對不上 Wikibooks 那列（它存的是「数据」），但打得到 zhtw-mcp 那列，反過來也一樣。  <!-- zhtw-lint: skip -->

**授權標示範例**：

- 來源：Wikibooks《大陸台灣計算機術語對照表》（CC BY-SA 4.0，https://creativecommons.org/licenses/by-sa/4.0/ ）
- 來源：sysprog21/zhtw-mcp（MIT），內含 OpenCC 詞庫（Apache-2.0）

**欄位**（依序，第一欄是英文）：

| 欄 | 內容 |
|----|------|
| `en` | 英文原文 |
| `tw` | 台灣用語 |
| `cn` | 要避開的寫法 |
| `type` | 資料來源與規則種類，見上表 |
| `clues` | 出現這些詞才成立（以「；」分隔） |
| `avoid_clues` | 出現這些詞就不成立 |
| `note` | 為什麼要改、限用於哪個語境 |

`cn` 欄的方向不是每一列都一樣，要連 `type` 一起讀：`confusable` 列放的是**台灣用語被用錯義項**（「函式」在程式設計正確，在數學該用「函數」），`disabled` 列則是刻意記下「這組看起來像錯、但不要改」。

**統計**：

- 資料列：2,122（glossary 447、cross_strait 1,602、variant 48、confusable 18、political_coloring 5、disabled 2）
- 大小：157 KB
- 格式：CSV（UTF-8）、LF 換行

用 grep 查，**不要整份讀**。整份讀進 context 超過四萬 token，只為換幾行結果。

```bash
# 依英文術語查
grep -i "array" terms.csv

# 依台灣術語查
grep "陣列" terms.csv

# 可疑詞是繁體時，繁簡兩形都打一次才不會漏
grep -n '數據\|数据\|組件\|组件' terms.csv
```

**多義詞**：同一個英文詞若有兩個義項，會出現兩列。`Comment (code)`、`Flush (align)`、`Token (security/currency)` 這三個義項標註是手動加的，重抓 glossary 會蓋掉，先 diff 再覆蓋。

**更新**：見 `../scripts/`。

---

**最後更新**：2026-08-09
