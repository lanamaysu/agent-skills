---
name: taiwan-traditional-chinese
description: Use when the user requests Chinese or Traditional Chinese output for responses, comments, docs, or localization, following Taiwan terminology (zh-Hant-TW/zh-TW/zh_TW).
---

# Taiwan Traditional Chinese Response Skill

台灣繁體中文回應指南。

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

## 品質檢查與重寫流程

1. 先產出草稿，再執行品質檢查。
2. 若出現下列禁用詞，視為不通過：
	`組件`、`组件`、`異步`、`异步`、`回退`、`代碼`、`代码`、`變量`、`变量`、`映射`、`對象`、`对象`、`數組`、`数组`、`函數`、`函数`、`參數`、`参数`、`返回值`、`導入`、`导入`、`導出`、`导出`、`依賴`、`依赖`、`數據`、`数据`、`應用程序`、`应用程序`、`數據庫`、`数据库`、`服務器`、`服务器`、`緩存`、`缓存`、`網絡`、`网络`。
3. 通過品質檢查：不要開啟 guidelines.md 與 terms.csv。
4. 未通過品質檢查：讀取 guidelines.md 與 terms.csv 進行嚴格術語稽核並重寫。
5. 最終輸出只提供通過版本，不要提及檢查或重寫過程。

## Minimal Example

```markdown
使用 React，在 `useEffect()` 中載入資料。
檔案位於 `src/components/Button.tsx`。
```

## Quick Checklist

- 繁體中文（zh-Hant-TW）
- 品質檢查通過（無禁用詞）
- 台灣術語
- 英文專有名詞保留
- 全形句子標點、半形程式碼標點
- 程式碼與檔名加反引號

## References

- [guidelines.md](./references/guidelines.md) - 完整指南
- [terms.csv](./references/terms.csv) - 術語對照表
- [Wikibooks 對照表](https://zh.wikibooks.org/zh-tw/%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8) - CC BY-SA 4.0
- [教育部重編國語辭典](https://dict.revised.moe.edu.tw/)

**Last Updated**: 2026-02-10

