---
title: Technical Terms to Preserve in English
impact: HIGH
category: language-standards
# 保留英文的技術術語

核心原則：框架名稱、API、檔案路徑、程式碼符號一律保留英文；中文只用在敘述與註解。

## 必保留英文的項目
- 框架/函式庫：React、Vue、Next.js、Node.js
- Hook/API：`useState`、`useEffect`、API、endpoint、request、response
- 檔案與程式碼：`src/components/Button.tsx`、className、function/variable 名稱、`const`/`async`/`await`
- 縮寫：HTML、CSS、JS、TS、JSON、URL、HTTP、REST、GraphQL、CI/CD、IDE

## 精簡範例
```javascript
// 保留英文關鍵字與路徑，註解用繁中
import { useState, useEffect } from 'react'

// 初始化使用者狀態
const [user, setUser] = useState(null)

useEffect(() => {
  // 呼叫 API 取得資料
  fetch('/api/users')
}, [])

// ✗ 過度翻譯（不要這樣）
// 使用 「狀態」掛鉤 來管理「使用者」
// 在 「效果」 中呼叫 應用程式介面
```

## 回應前檢查
- [ ] 框架/Hook/縮寫未翻譯（React、useState、API、URL）
- [ ] 檔名、變數、程式碼符號保持英文
- [ ] 中文只用在描述與註解，避免音譯或自創翻譯
- [ ] Abbreviations in English: HTML, CSS, JS, JSON, URL
- [ ] Code keywords preserved: `const`, `async`, `import`, `export`
- [ ] Comments can be in Chinese, but code stays English

## 不確定時的原則

> **經驗法則**：不確定時就保留英文。保持技術清晰度比強行翻譯造成混淆更重要。

```javascript
// 不確定時保留英文
✓ 在 React 中使用
✗ 在 瑞克特 中使用
```
