---
name: taiwan-traditional-chinese
description: READ FIRST before ANY Traditional Chinese output (files, docs, markdown, comments, translations). Taiwan zh_TW terminology standards. Must read when creating content, writing documentation, or responding in Chinese.
---

# Taiwan Traditional Chinese Response Skill

台灣繁體中文回應指南。

## 🔴 MANDATORY PRE-CHECK

**Before generating ANY Traditional Chinese content, you MUST:**

1. ✅ Read `terminology-core.md` for common terms
2. ✅ Check this skill's "When to Use" section
3. ✅ Verify terminology against Taiwan conventions

**Common mistakes when NOT reading this skill:**

- ❌ 代碼 → ✅ 程式碼
- ❌ 数据 → ✅ 資料
- ❌ 组件 → ✅ 元件
- ❌ 应用程序 → ✅ 應用程式
- ❌ 数据库 → ✅ 資料庫
- ❌ 服务器 → ✅ 伺服器

---

## Quick Reference (快速參考)

### Core Principles

| 原則 | 說明 | 例子 |
|------|------|------|
| **字體** | 繁體中文（zh_TW），非簡體 | ✓ 資料 ✗ 数据 |
| **術語** | 台灣慣例 | ✓ 應用程式 ✗ 应用程序 |
| **英文** | 保留框架和程式碼 | ✓ React state ✗ 瑞克特狀態 |
| **標點** | 句子全形、程式碼半形 | ✓ 設定後。 ✗ 設定後。) |
| **語氣** | 專業且親切 | ✓ 我建議... ✗ 茲建議閣下... |

## When to Use

- 使用者以台灣繁體中文提問或要求中文輸出
- 撰寫或審查文件、註解、提交訊息時需遵守台灣術語
- 介面文案、在地化內容、翻譯或測試中文呈現時
- 需要統一技術術語、標點與語氣風格的場合

---

## Rules Index (規則索引)

| Rule File | 內容 | 優先度 |
|-----------|------|--------|
| [terminology-core.md](./rules/terminology-core.md) | 核心術語與領域精選 | **HIGH** |
| [technical-terms-preserve.md](./rules/technical-terms-preserve.md) | 保留英文的技術詞彙清單 | **HIGH** |
| [punctuation-and-formatting.md](./rules/punctuation-and-formatting.md) | 標點符號、格式化、間距規則 | **HIGH** |
| [practical-examples.md](./rules/practical-examples.md) | 程式碼、提交訊息、錯誤訊息範例 | MEDIUM |

## Steps

1. 先閱讀 [terminology-core.md](./rules/terminology-core.md) 確認核心與領域精選術語。
2. 視需求查閱需保留英文的清單（technical-terms-preserve）。
3. 套用標點與格式規則：句子全形、程式碼半形。
4. 保持專業但親切的語氣，避免過度翻譯或使用非台灣慣用詞。
5. 回覆前使用「Quality Checklist」逐項檢查。

---

## Quick Examples

### ✓ Correct Usage

```javascript
// 程式碼保持英文，註解用中文
// 初始化使用者狀態
const [user, setUser] = useState(null)

// 匯入 React hook
import { useEffect } from 'react'

// 呼叫 API endpoint 取得資料
const response = await fetch('/api/users')
```

```markdown
# 説明文檔

在 React component 中使用 `useState` hook 來管理狀態。

使用 `async/await` 語法簡化非同步程式碼。

設定環境變數後，啟動伺服器。
```

### ✗ Common Mistakes

```javascript
// ✗ 過度翻譯
const [使用者, 設置使用者] = useState(null)

// ✗ 混用 Mainland 術語
// 初始化用户状态
const [user, setUser] = useState(null)

// ✗ 標點混亂
使用 `useState` hook 來管理狀態。但要注意 dependency
```

---

## Core Principles Explained

### 1. Use Traditional Chinese

**Rule**: 必須使用台灣繁體中文（zh_TW）。

```markdown
✓ 正確: 資料、應用程式、伺服器、執行緒、演算法
✗ 錯誤: 数据、应用程序、服务器、线程、算法 (Mainland)
✗ 錯誤: 資料、應用程式、伺服器 (Hong Kong variation)
```

詳見: [terminology-core.md](./rules/terminology-core.md)

### 2. Preserve English Technical Terms

**Rule**: 框架名稱、Hook、API 術語等保留英文。

```markdown
✓ 使用 React 中的 useState
✓ 呼叫 /api/users endpoint
✓ 在 useEffect 中處理 side effects

✗ 使用 瑞克特 中的 使用狀態
✗ 呼叫 應用程式介面 使用者
```

詳見: [technical-terms-preserve.md](./rules/technical-terms-preserve.md)

### 3. Correct Punctuation

**Rule**: 句子用全形、程式碼用半形。

```markdown
✓ 設定 80px 寬度。
✓ 檔案路徑為 `src/components/Button.tsx`
✓ 執行 `fetchData()` 函式。

✗ 設定 80px 寬度。) (全形括號)
✗ 檔案路徑為 "src/components/Button.tsx" (英文引號)
✗ 執行 `fetchData（）` 函式。(全形括號)
```

詳見: [punctuation-and-formatting.md](./rules/punctuation-and-formatting.md)

### 4. Terminology Consistency

**Rule**: 選定術語後保持一致，避免混用 Mainland/Taiwan 用語。

| Context | Taiwan | Mainland | 避免混用 |
|---------|--------|----------|---------|
| 數據 | 資料 | 数据 | ✓ 統一用「資料」 |
| 更新 | 更新 | 更新 | ✓ 相同（都可用） |
| 載入 | 載入 | 加载 | ✓ 統一用「載入」 |

詳見: [terminology-core.md](./rules/terminology-core.md)

## Real Examples

### Git Commit Message

```bash
# ✓ Correct format (Taiwan Chinese + English terms)
git commit -m "feat(member): 新增使用者編輯功能"
git commit -m "fix: 修正 component 不斷重新 render 的問題"
git commit -m "docs: 更新 README 中的安裝指南"

# ✗ Wrong
git commit -m "feat: update stuff"  (English, unclear)
git commit -m "feat: 新增功能、修復錯誤，並更新文檔"  (>50 chars)
```

詳見: [practical-examples.md](./rules/practical-examples.md)

### Code Comments

```javascript
// ✓ Good
// 初始化使用者狀態
const [user, setUser] = useState(null)

// 呼叫後端 API 更新使用者資訊
const response = await updateUserAPI(formData)

// ✗ Wrong
// 初始化用户状态 (Mainland term)
// 处理表单提交 (Too vague, Mainland term)
```

詳見: [practical-examples.md](./rules/practical-examples.md)

---

## Quality Checklist

Before responding in Taiwan Traditional Chinese:

- [ ] 使用繁體中文（zh_TW），非簡體（简体）
- [ ] 技術術語符合台灣慣例（資料、應用程式等）
- [ ] 英文專有名詞保留：React、useState、API、endpoint 等
- [ ] 句子使用全形標點符號（。，？！）
- [ ] 程式碼使用半形標點符號
- [ ] 語氣專業但親切，可執行
- [ ] 避免過度翻譯和 Mainland 術語
- [ ] 範例清晰且可直接應用

---

## Integration Guidelines

此技能適用於任何需要台灣繁體中文的專案：

- 遵循台灣慣例的技術術語
- 支援雙語方式（英文程式碼、中文文檔/註解）
- 適用於 commit messages、文檔、使用者介面等
- 提供台灣導向的使用者體驗

**專案整合建議**：如專案有 AGENTS.md 或類似指南，建議在「中文撰寫規範」部分參照此技能。

---

## Compatibility

- 通用規範，未使用 agent 特定功能；適用任何支援 Agent Skills 的代理。
- 放置於標準技能搜尋路徑（如 `.claude/skills/`、`skills/` 等）即可被 add-skill 偵測。

## Troubleshooting

- 若代理未載入：確認 `SKILL.md` frontmatter 具備 `name`、`description`，且路徑在支援目錄。
- 若 add-skill 顯示找不到技能：確保資料夾含有效 `SKILL.md` 並非空白；必要時使用完整 repo 路徑或 tag（例如 `...#v1.0.0`）。
- 若特定代理（如 Kiro/OpenHands）需額外設定，請依該代理的技能文件加入資源路徑。

---

## References

### Local Resources

- 📁 [Complete Terminology CSV](./references/terms.csv) - 460+ 技術術語對照表（Wikibooks 抓取，自動產出）
- 📄 [References README](./references/README.md) - 來源、授權（CC BY-SA 4.0）、更新方式說明；重新產生 CSV：`.venv/bin/python references/fetch_terms.py`

### External Resources

- [大陸台灣計算機術語對照表（Wikibooks, CC BY-SA 4.0）](https://zh.wikibooks.org/zh-tw/%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8)
- [Taiwan MOE](https://www.moe.gov.tw/en/) - Taiwan Ministry of Education language standards
- [教育部重編國語辭典修訂本](https://dict.revised.moe.edu.tw/) - Official Taiwan dictionary

---

**Last Updated**: 2026-01-23
