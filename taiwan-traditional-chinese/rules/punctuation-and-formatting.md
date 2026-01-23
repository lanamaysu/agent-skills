---
title: Punctuation and Formatting Rules
impact: HIGH
category: formatting-standards
tags: punctuation, formatting, typography, zh-tw
---

# 標點符號與格式規則

核心：句子用全形，程式碼用半形；程式碼與檔名需反引號包住。

## 必備示例

```markdown
# ✓ Correct
使用 React 框架，並在 `useEffect()` 中處理資料載入。
檔案位於 `src/components/Button.tsx`。
執行：`pnpm install` 後 `pnpm dev`。

# ✗ Wrong
使用 React 框架。並在 useEffect（）中處理資料載入。（全形括號、缺反引號）
檔案位於 src/components/Button。tsx。（句號混入檔名）
```

## 句子 vs 程式碼

- 中文敘述：全形標點（。，？！）。
- 程式碼/指令/路徑：半形標點；以反引號或程式碼區塊標示。

```javascript
// ✓ 半形標點
fetchData(id, options)
const path = 'src/components/Button.tsx'

// ✗ 全形標點
fetchData（id，options）
```

## 空白與間距
- 中英文間建議留一個半形空格：使用 React 開發應用。
- 反引號內外不要多餘空格：`useState`、`/api/users`。

## 數字與單位
- 技術語境用半形數字與單位：80px、100%。
- 敘述步驟可用「第一步、第二步」等全形數字亦可。

## 列表與區塊
- 列表風格一致（同樣使用 1./-），程式碼區塊務必指定語言：```bash / ```javascript。

## 強調
重要：「必須在 component 最上層呼叫 hooks」。

## 引用程式碼
他說：「使用 `useState` 來管理狀態」。

# ✗ Wrong
"這是引號"（英文雙引號）
'這是單引號'（英文單引號）
```

---

## Bullet Points (項目符號)

```markdown
# ✓ Good

## 正確做法
✓ 使用 `getByRole` 查詢元素
✓ 在 `userEvent` 中模擬互動
✓ 用 `findBy` 等待非同步結果

## 要避免的做法
✗ 使用 `getByTestId` 作為首選
✗ 使用 `fireEvent` 而非 `userEvent`
```

---

## Quick Checklist

格式化繁中內容前檢查：

- [ ] 句子用全形標點（。，？！）
- [ ] 程式碼用半形標點
- [ ] Inline code 用反引號 \`code\`
- [ ] Code blocks 指定語言
- [ ] 中英之間適當間距
- [ ] 引號使用「」而非 ""
- [ ] 數字在技術語境用半形
- [ ] 列表格式一致
- [ ] 連結格式正確
