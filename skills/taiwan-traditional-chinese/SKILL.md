---
name: taiwan-traditional-chinese
description: Use when the user requests Chinese or Traditional Chinese output for responses, comments, docs, or localization, following Taiwan terminology (zh-Hant-TW/zh-TW/zh_TW).
---

# Taiwan Traditional Chinese Response Skill

> **TL;DR**
> - 必用台灣術語：元件、非同步、資料、伺服器、資料庫、快取，框架與程式碼維持英文。
> - 絕對禁用：組件/组件、異步/异步、數據/数据、服務器/服务器、函數/函数、數組/数组、加載、依賴。

## Required Pre-Check

- Do NOT read [guidelines.md](./references/guidelines.md) before the quality check.
- Only read [guidelines.md](./references/guidelines.md) after the quality check fails, or when the user explicitly asks for a strict term audit.
- Do NOT read [terms.csv](./references/terms.csv) before the quality check.
- Only read [terms.csv](./references/terms.csv) after the quality check fails, or when the user explicitly asks for a strict term audit.
- Explicit audit trigger phrases (examples): "請做術語檢查" / "請做用詞審查" / "請嚴格對照 terms.csv".

## Core Rules

- 使用繁體中文（zh-Hant-TW/zh-TW/zh_TW），並且使用在地話詞語。
- 若使用者說「用中文／中文回答／中文輸出」，一律視為繁體中文（zh-Hant-TW），除非明確指定簡體（簡體／简体／zh-Hans／简中）。
- 術語用台灣慣例（資料、元件、應用程式、資料庫、伺服器）。
- 框架名稱、API、程式碼符號、檔案路徑保留英文。
- 檔案路徑不要做成連結，直接用反引號。
- 句子用全形標點，程式碼與路徑用半形標點。
- 程式碼與檔名用反引號包住。

## 關鍵術語速查表（必須遵守）

**絕對禁用**：代碼、组件、異步/异步、回退、代碼/代码、變量/变量、映射、對象/对象、數組/数组、函數/函数、返回值、導入/导入、導出/导出、依賴/依赖、數據/数据、應用程序/应用程序、數據庫/数据库、服務器/服务器、緩存/缓存、網絡/网络、加載、模塊、線程

**必用台灣術語**：
- component → **元件**（不是「組件」）
- array → **陣列**（不是「數組」）
- object → **物件**（不是「對象」）
- function → **函式**（不是「函數」）
- data → **資料**（不是「數據」）
- variable → **變數**（不是「變量」）
- parameter → **參數**（不是「参数」）
- return value → **回傳值**（不是「返回值」）
- import → **匯入**（不是「導入」）
- export → **匯出**（不是「導出」）
- async → **非同步**（不是「異步」）
- cache → **快取**（不是「緩存」）
- load → **載入**（不是「加載」）
- server → **伺服器**（不是「服務器」）
- database → **資料庫**（不是「數據庫」）
- network → **網路**（不是「網絡」）
- thread → **執行緒**（不是「線程」）
- module → **模組**（不是「模塊」）
- package → **套件**（不是「包」）
- dependency → **相依性**（不是「依賴」）

## 品質檢查與重寫流程

### 較小模型（Haiku, GPT-4o mini）
- **直接使用上方「關鍵術語速查表」**，第一次就用對術語
- 不需要草稿檢查流程，參考速查表直接產出正確輸出
- 只有使用者明確要求術語稽核（「請做術語檢查」）時，才讀取 guidelines.md 和 terms.csv

### 較大模型（Sonnet, Opus, GPT-4）
1. 先產出草稿，再執行品質檢查
2. 若出現上方「絕對禁用」列表中的詞，視為不通過
3. 通過品質檢查：不要開啟 guidelines.md 與 terms.csv
4. 未通過品質檢查：讀取 guidelines.md 與 terms.csv 進行嚴格術語稽核並重寫
5. 最終輸出只提供通過版本，不要提及檢查或重寫過程

## Minimal Example

```markdown
使用 React，在 `useEffect()` 中載入資料。
檔案位於 `src/components/Button.tsx`。
```

## Quick Checklist

- 繁體中文（zh-Hant-TW）
- **參考關鍵術語速查表**（Haiku/小模型必看）
- 無禁用詞（組件、異步、數據、服務器等）
- 台灣術語（元件、非同步、資料、伺服器）
- 英文專有名詞保留（React、useState、API）
- 全形句子標點、半形程式碼標點
- 程式碼與檔名加反引號

## References

- **[關鍵術語速查表](#關鍵術語速查表必須遵守)** - 小模型必看 ⭐
- [guidelines.md](./references/guidelines.md) - 完整指南（大模型或明確稽核時使用）
- [terms.csv](./references/terms.csv) - 術語對照表（460+ 筆）
- [Wikibooks 對照表](https://zh.wikibooks.org/zh-tw/%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8) - CC BY-SA 4.0
- [教育部重編國語辭典](https://dict.revised.moe.edu.tw/)

**Last Updated**: 2026-02-11

