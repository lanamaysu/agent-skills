# Taiwan Traditional Chinese Guidelines

完整的台灣繁體中文技術寫作指南。只在 `SKILL.md` 的品質檢查未通過、或使用者明確要求術語稽核時讀。

| 章節 | 內容 |
|------|------|
| [核心術語對照](#核心術語對照) | 必知術語表、容易混淆的詞、領域術語（Web / DB / UI / System） |
| [保留英文的技術術語](#保留英文的技術術語) | 哪些不要翻、英文命名禁止無意義音譯 |
| [標點符號與格式](#標點符號與格式) | 全形半形、空白、反引號 |
| [實務範例](#實務範例) | 程式碼註解、commit 訊息、錯誤訊息、文件 |
| [中國用語過濾](#中國用語過濾表外詞彙與非-it-領域) | 怎麼 grep terms.csv、學術職場與日常對照表、表外判斷原則 |
| [常見錯誤](#常見錯誤) | 四類典型錯誤的對照 |
| [參考資源](#參考資源) | 來源與授權 |

---

## 核心術語對照

根據 Wikibooks《大陸台灣計算機術語對照表》（CC BY-SA 4.0）

> **完整對照表**：[terms.csv](./terms.csv)，2,122 筆術語（自動從 Wikibooks 與 zhtw-mcp ruleset 抓取）

### 必知術語

最常用的技術詞彙：

| Taiwan (✓) | Mainland (✗) | English |
|------------|--------------|---------|
| 元件 | 组件 | component |
| 陣列 | 数组 | array |
| 物件 | 对象 | object |
| 函式 | 函数 | function |
| 資料 | 数据 | data |
| 應用程式 | 应用程序 | application |
| 資料庫 | 数据库 | database |
| 伺服器 | 服务器 | server |
| 執行緒 | 线程 | thread |
| 演算法 | 算法 | algorithm |
| 網路 | 网络 | network |
| 程式碼 | 代码 | code |
| 快取 | 缓存 | cache |
| 瀏覽器 | 浏览器 | browser |
| 捲動 | 滚动 | scroll |
| 下拉式選單 | 下拉菜单 | dropdown menu |
| 變數 | 变量 | variable |
| 參數 | 参数 | parameter |
| 回傳值 | 返回值 | return value |
| 匯入 | 导入 | import |
| 匯出 | 导出 | export |
| 套件 | 包 | package |
| 相依性 | 依赖 | dependency |

### 容易混淆的術語

- **數據 vs 資料**：台灣用「資料」；「數據」指數字型資料，較少單獨使用
- **更新 vs 修改**：資料改變用「更新」；配置參數用「修改」或「調整」
- **載入 vs 加載**：台灣用「載入」；「加載」是 mainland 術語
- **模組 vs 模塊**：台灣用「模組」；「模塊」是 mainland 術語

### 領域術語精選

**Web**
- 前端 frontend / 後端 backend / 端點 endpoint
- 請求 request / 回應 response / 網域 domain / 埠 port

**Database**
- 資料表 table / 欄位 field / 紀錄 record
- 主鍵 primary key / 外來鍵 foreign key
- 備份 backup / 還原 restore

**UI/UX**
- 按鈕 button / 輸入框 input field / 下拉選單 dropdown
- 核取方塊 checkbox / 彈出視窗 modal/popup
- 索引標籤/分頁 tab

**System & Tools**
- 作業系統 operating system / 記憶體 memory
- 行程 process / 執行緒 thread / 容器 container
- 版本控制 version control / 儲存庫 repository

---

## 保留英文的技術術語

**核心原則**：框架名稱、API、檔案路徑、程式碼符號一律保留英文；中文只用在敘述與註解。

### 必保留英文

- **框架/函式庫**：React、Vue、Next.js、Node.js、Express
- **Hook/API**：`useState`、`useEffect`、API、endpoint、request、response
- **檔案與程式碼**：`src/components/Button.tsx`、className、function/variable 名稱、`const`/`async`/`await`
- **縮寫**：HTML、CSS、JS、TS、JSON、URL、HTTP、REST、GraphQL、CI/CD、IDE

### 範例

```javascript
// ✓ 保留英文關鍵字與路徑，註解用繁中
import { useState, useEffect } from 'react'

// 初始化使用者狀態
const [user, setUser] = useState(null)

useEffect(() => {
  // 呼叫 API 取得資料
  fetch('/api/users')
}, [])
```

```javascript
// ✗ 過度翻譯（不要這樣）
// 使用「狀態」掛鉤來管理「使用者」
// 在「效果」中呼叫應用程式介面
```

### 經驗法則

> 不確定時就保留英文。保持技術清晰度比強行翻譯造成混淆更重要。

### 英文命名禁止無意義音譯

為檔案、變數、分支、專案、skill、函式取英文名稱時，不要把中文詞彙用漢語拼音音譯充當英文（`ziliao-loader`、`yuanjian-utils`、`de-ai-wei`）。這是中國常見的命名習慣，對不諳中文的人是一串無意義音節，也讓 grep 與自動補全失去語意線索。用語意對應的真實英語詞彙：`data-loader`、`component-utils`、`de-ai-tone`。

例外：本來就以音譯通行的專有名詞不在此限，例如人名、地名（Taipei）、以及英語文獻已約定俗成的詞（qi、yin-yang）。判準是：英語讀者查得到這個詞嗎？查不到就翻譯，查得到就沿用。

---

## 標點符號與格式

**核心原則**：句子用全形，程式碼用半形；程式碼與檔名需反引號包住。

### 基本規則

**句子 vs 程式碼**
- 中文敘述：全形標點（。，？！）
- 程式碼/指令/路徑：半形標點；以反引號或程式碼區塊標示

**空白與間距**
- 中英文間建議留一個半形空白：使用 React 開發應用。
- 反引號內外不要多餘空白：`useState`、`/api/users`

**數字與單位**
- 技術語境用半形數字與單位：80px、100%
- 敘述步驟可用全形數字：第一步、第二步

**引號**
- 中文引用：「」（全形單引號）
- 程式碼：反引號 `` ` ``

### 範例

```markdown
# ✓ Correct
使用 React 框架，並在 `useEffect()` 中處理資料載入。
檔案位於 `src/components/Button.tsx`。
執行：`pnpm install` 後 `pnpm dev`。

# ✗ Wrong
使用 React 框架。並在 useEffect（）中處理資料載入。（全形括號、缺反引號）
檔案位於 src/components/Button。tsx。（句號混入檔名）
執行："pnpm install" 後 "pnpm dev"。（英文引號）
```

```javascript
// ✓ 半形標點
fetchData(id, options)
const path = 'src/components/Button.tsx'

// ✗ 全形標點
fetchData（id，options）
```

---

## 實務範例

### 程式碼註解

```javascript
// ✓ Good
// 初始化使用者狀態
const [user, setUser] = useState(null)

// 呼叫後端 API 更新使用者資訊
const response = await updateUserAPI(formData)

// ✗ Wrong
// 初始化用户状态 (Mainland 術語)
// 使用「使用狀態」掛鉤來管理狀態 (過度翻譯)
```

### Commit 訊息

推薦格式：`type(scope): 簡短描述`

```bash
# ✓ Good
feat(member): 新增使用者編輯功能
fix: 修正 component 不斷重新 render 的問題
docs: 更新 README 中的安裝指南

# ✗ Wrong
feat: update stuff  (英文、不清楚)
feat: 新增功能、修復錯誤，並更新文檔  (超過 50 字元)
feat(member): 新增用户编辑功能  (Mainland 術語)
```

### 錯誤訊息

```javascript
// ✓ Good - 清楚友善
throw new Error('無法載入使用者資訊，請稍後再試')
throw new Error('檔案格式不正確，請上傳 JSON 檔案')

// ✗ Wrong
throw new Error('Error loading user')  (全英文)
throw new Error('加载用户信息失败')  (Mainland 術語)
```

### 文件撰寫

```markdown
# ✓ Good
使用 `useState` 管理 state。檔案：`src/components/Button.tsx`。

在 React component 中使用 `useEffect` hook 來處理 side effects。

# ✗ Wrong
使用「使用狀態」掛鉤取得使用者資料。(過度翻譯)
使用 useState 管理 state (缺反引號)
使用 `useState` 管理状态。(Mainland 術語)
```

---

## 中國用語過濾：表外詞彙與非 IT 領域

「繁體字形」不等於「台灣用語」：把簡體轉成繁體字形後，詞彙仍可能是中國大陸用語。[terms.csv](./terms.csv) 以 IT 術語為主，下面補的是它抓不到的兩類：跨出 IT 領域的日常與學術用語，以及表外詞彙的判斷方法。

### 怎麼 grep terms.csv

terms.csv 是 2,122 筆術語的查詢表，**用 `grep` 查，不要整份讀**（整份讀超過四萬 token）。它的 `cn` 欄兩種字形都有：Wikibooks 來的那批（`type` 為 `glossary`）存簡體，zhtw-mcp 來的那批存繁體。所以：

```bash
# 繁簡兩形都打一次，只打一種會漏掉另一批來源
grep -n '數據\|数据\|組件\|组件' references/terms.csv

# 命中後看 clues／avoid_clues／note 三欄：那是判斷條件，不是註解
grep -n ',項目,' references/terms.csv
```

`type` 是 `disabled` 的列意思相反：那是刻意記下「看起來像錯、但不要改」的組合（`參數`、`文件`）。`confusable` 列的 `cn` 欄放的是台灣用語被用錯義項，不是中國用語。

### 學術與職場

| 禁用 | 使用 |
|------|------|
| 水平（=標準） | 水準（「水平」僅保留 horizontal 之義） |
| 通過（=藉由） | 透過 / 藉由（「通過」保留 pass 之義） |
| 渠道 | 管道 |
| 領導（名詞，=上司） | 主管 |
| 課題 | 研究題目 / 專案 |
| 本科 | 大學部 / 學士班 |
| 導師（研究所） | 指導教授 |
| 答辯 | 口試 |
| 網課 | 線上課程 |

### 日常

| 禁用 | 使用 |
|------|------|
| 短信 / 郵箱 | 簡訊 / 信箱 |
| 立馬 | 馬上 / 立刻 |
| 出租車 / 打車 | 計程車 / 叫車 |
| 公交 | 公車 |
| 視頻 / 音頻 | 影片（內容）/ 視訊（通訊）/ 音訊 |
| 二維碼 | QR code |
| 充電寶 / U盤 | 行動電源 / 隨身碟 |
| 博客 | 部落格 |

### 表外詞彙的判斷原則

對照表不可能窮盡。遇到表外的疑似中國用語時：

1. **以台灣慣用為先**。教育部辭典、台灣學術界與媒體的通行用法優先。不確定時，選台灣讀者不會皺眉的那個。
2. **一詞多義要看義項**。「質量」「水平」「通過」「項目」不是全面禁用，是特定義項禁用；翻譯物理文獻時 mass 當然譯「質量」。完整清單見 [SKILL.md](../SKILL.md) 的「一詞多義」表。
3. **已歸化的借詞從寬**。「網紅」「打卡」「吐槽」已進入台灣日常語彙，可視語域使用；正式文件仍避免。
4. **語法層面的陸腔也要防**。「挺好的」→「蠻好的 / 很好」；「⋯⋯來著」刪除；萬用動詞「整」「搞」在正式文件中改成具體動詞。

---

## 常見錯誤

### 術語混用
❌ 数据、应用程序、服务器 (Mainland)
✅ 資料、應用程式、伺服器 (Taiwan)

### 標點混亂
❌ 使用 `useState` hook。但要注意 dependency (半形句號、缺全形標點)
✅ 使用 `useState` hook。但要注意 dependency。

### 過度翻譯
❌ 在「瑞克特」中使用「使用狀態」掛鉤
✅ 在 React 中使用 `useState`

### 檔名處理
❌ 檔案位於 src/components/Button.tsx (缺反引號)
✅ 檔案位於 `src/components/Button.tsx`

---

## 參考資源

- [terms.csv](./terms.csv)：完整術語對照表（2,122 筆）。由 [scripts/fetch_terms.py](../scripts/fetch_terms.py) 從下方兩個來源重新產生；重跑 glossary 會蓋掉手動加的義項標註（`Comment (code)`、`Flush (align)`、`Token (security/currency)`）與 Token 的 cn 欄修正，先 diff 再覆蓋
- [prose-style.md](./prose-style.md)：去 AI 味的行文規範（寫連續散文時使用）
- [Wikibooks 對照表](https://zh.wikibooks.org/zh-tw/%E5%A4%A7%E9%99%86%E5%8F%B0%E6%B9%BE%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%9C%AF%E8%AF%AD%E5%AF%B9%E7%85%A7%E8%A1%A8)：CC BY-SA 4.0
- [sysprog21/zhtw-mcp](https://github.com/sysprog21/zhtw-mcp)：MIT，`assets/ruleset.json` 是 terms.csv 消歧義欄位的來源，跨海峽詞條再上溯 [OpenCC](https://github.com/BYVoid/OpenCC)（Apache-2.0）
- [教育部重編國語辭典](https://dict.revised.moe.edu.tw/)：官方辭典
- [allenloves/de-ai-tone](https://github.com/allenloves/de-ai-tone)：CC BY-SA 4.0，「中國用語過濾」與命名規則的來源
