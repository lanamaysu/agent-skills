---
title: Practical Examples and Patterns
impact: MEDIUM
category: examples
tags: patterns, examples, use-cases, zh-tw
---

# 實務範例與模式

## 程式碼註解
```javascript
// 初始化使用者狀態
const [user, setUser] = useState(null)

// ✗ 不要翻譯技術術語
// 使用「使用狀態」掛鉤來管理狀態
```

## Commit 訊息
推薦：`type(scope): 簡短描述`
```bash
# ✓
feat(member): 新增使用者編輯功能
fix: 修正 component 重複 render
# 實務範例與模式（極簡版）

## 最小示例
```javascript
// 程式碼用英文，註解用繁中
const [user, setUser] = useState(null)  // 初始化使用者狀態
```

```bash
# Commit：type(scope): 描述（簡短、用台灣術語）
feat(member): 新增使用者編輯功能
# ✗ update stuff
```

```javascript
// 錯誤訊息：清楚友善
throw new Error('無法載入使用者資訊，請稍後再試')
```

```markdown
使用 `useState` 管理 state，檔案：`src/components/Button.tsx`。
// ✗ 使用「使用狀態」掛鉤取得使用者資料。
```

## 常見錯誤（只記兩條）
- 術語混用：資料/應用程式/伺服器（避免 数据/应用程序/服务器）。
- 標點混亂：程式碼半形、句子全形；檔名與程式碼要加反引號。

## 快速檢查
- [ ] 術語採台灣用法，技術詞保留英文
- [ ] 句子全形標點，程式碼半形並加反引號
- [ ] Commit/訊息簡潔可讀
- [ ] 錯誤訊息清楚友善
