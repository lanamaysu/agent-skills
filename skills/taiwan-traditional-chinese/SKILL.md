---
name: taiwan-traditional-chinese
description: 'Taiwan Traditional Chinese (zh-Hant-TW) house style: terminology, punctuation, de-AI tone. Judge by the deliverable, not keywords — if your output will contain Chinese, this applies; read it before the first Chinese character, not after. A git, React or JSON task counts once its output is Chinese: commit messages, PR descriptions, ADRs, README, specs, slide decks, code comments, test-case names, zh-TW locale files. Not for ephemeral chat replies, which follow the conversation style rules already in effect. Also for repairing Chinese: mainland wording (數據/組件), mainland software-industry jargon (落地/對齊/閉環), Taiwan terms (元件/資料/函式), AI 味. Default zh-Hant-TW unless 簡體 is asked. Skip when Chinese is the bug not the output (fonts, encoding, full-width spacing, 繁簡轉換) or when translating into another language.'
---

# Taiwan Traditional Chinese Response Skill

> **TL;DR**
> - 必用台灣術語：元件、非同步、資料、伺服器、資料庫、快取；框架與程式碼維持英文。
> - 絕對禁用：組件/组件、異步/异步、數據/数据、服務器/服务器、函數/函数、數組/数组、加載、依賴。  <!-- zhtw-lint: skip -->
> - 一看到就刪：值得注意的是、事實上、總的來說、賦能、深入探討、打造、至關重要、進行 + 動詞。

## Required Pre-Check

本檔的四張表常時生效，references 預設不讀。

- **[prose-style.md](./references/prose-style.md)**：寫連續散文才讀（專案文件、README 敘述段落、ADR、release note、規格書、簡報，或使用者說「太像 AI」「潤稿」）。要讀就在動筆前讀，不是寫完再回頭校對：稿子的段落結構一旦成形就很難拆，事後校對只改得動詞彙。實測讓模型自行安排順序，它會把這份排到最後一個動作，三篇稿子的骨架那時早就定了。commit message、程式碼註解、測試案例描述、表格與 API 參數說明不要讀：固定格式套散文節奏會壞掉，本檔的「AI 味速查」那層已經夠。
- 不要照抄本檔的外觀。本檔為了查閱方便用了大量粗體與表格，那是速查表的格式，不是你要產出的格式。散文就寫成散文：偽小標（獨立一行的 `**……**`）是明確禁止的，見下方「AI 味速查」第 4 條。
- **[guidelines.md](./references/guidelines.md)**：只在品質檢查未通過，或使用者要求稽核時讀。
- **[terms.csv](./references/terms.csv)**：**每次產出中文都要查，這是必要步驟**，做法見下方「品質檢查與重寫流程」第 2 步。永遠 `grep`，不要整份讀：2,122 筆術語，整份讀要四萬 token 以上，grep 只回幾列。

## Core Rules

- 使用繁體中文（zh-Hant-TW/zh-TW/zh_TW），並且使用在地慣用詞。
- 使用者說「用中文／中文回答／中文輸出」一律視為繁體中文，除非明確指定簡體（簡體／简体／zh-Hans／简中）。  <!-- zhtw-lint: skip -->
- 術語用台灣慣例（資料、元件、應用程式、資料庫、伺服器）。
- 框架名稱、API、程式碼符號、檔案路徑保留英文。
- 檔案路徑不要做成連結，直接用反引號包住。
- 中文句子用全形標點，程式碼與路徑用半形標點。

## 關鍵術語速查表（必須遵守）

**絕對禁用**：代碼/代码、组件、異步/异步、回退、變量/变量、映射、對象/对象、數組/数组、函數/函数、返回值、導入/导入、導出/导出、依賴/依赖、數據/数据、應用程序/应用程序、數據庫/数据库、服務器/服务器、緩存/缓存、網絡/网络、加載、模塊、線程  <!-- zhtw-lint: skip -->

**必用台灣術語**：component 元件、array 陣列、object 物件、function 函式、data 資料、variable 變數、parameter 參數、return value 回傳值、import 匯入、export 匯出、async 非同步、cache 快取、load 載入、server 伺服器、database 資料庫、network 網路、thread 執行緒、module 模組、package 套件、dependency 相依性

## 中國軟體圈行話禁用表（所有任務皆適用）

這些詞既是中國用語也是空話，換成具體動詞後句子會被迫說清楚到底做了什麼。寫專案文件、PR 描述、會議紀錄時最容易漏進來。

| 禁用 | 替代 |
|------|------|
| 落地 | 實作、實現、上線 |
| 復盤 | 檢討、回顧 |
| 沉澱（抽象物） | 累積、整理留存 |
| 閉環 | 完整流程；「形成閉環」→ 把流程走完 |
| 抓手 | 著力點、切入點 |
| 打通 | 整合、串接 |
| 顆粒度 | 細緻程度（技術文件的 granularity「粒度」可用） |
| 賽道 | 領域、市場 |
| 頭部（=領先者） | 龍頭、頂尖 |
| 痛點 | 台灣商業語境已通行；正式文件改「問題所在」「癥結」 |

## 一詞多義：看義項判斷，不是全面禁用

這幾個詞台灣也在用，只是義項不同，看義項判斷。下表是最常踩的幾個；其餘的查 terms.csv，`clues`／`avoid_clues`／`note` 三欄記的就是判斷條件。

| 詞 | 台灣保留的義項 | 這個義項要改 |
|----|----------------|--------------|
| 質量 | 物理學 mass | quality → **品質** |
| 水平 | horizontal | 標準、程度 → **水準** |
| 通過 | pass（通過考試、通過審查） | 藉由 → **透過 / 藉由** |
| 項目 | item（清單項目） | project → **專案** |
| 對齊 | 排版、資料結構對齊 | 會議上的「對齊」→ **同步、取得共識** |
| 數據 | 數值統計 | 泛稱 data → **資料** |
| 文件 | document | file → **檔案** |
| 並行 | concurrency | parallelism → **平行**（中國的「並行」指 parallel，照抄會反過來） |
| 進程 | 進度、進展 | OS process → **行程** |
| 渲染 | 誇大；國畫暈染技法 | rendering → **算繪** |
| 遍歷 | 遍歷理論（Ergodic theory） | traverse → **走訪** |

字形不影響判斷：「數據」「組件」「落地」寫成繁體之後還是中國用語。繁簡是字形問題，用詞是地域問題，上方三張表兩種字形都要改。（grep terms.csv 的細節見 guidelines.md）  <!-- zhtw-lint: skip -->

## AI 味速查（所有任務皆適用）

用詞對了，文字還是可能一看就知道是 AI 寫的。術語錯了同事會抓，AI 味沒人會抓，只會讓文件沒人想讀。

**一看到就刪**（刪掉語意不損，不必猶豫）：值得注意的是、需要注意的是、值得一提的是、更重要的是、事實上、毫無疑問、可以說、簡單來說、總的來說、綜上所述；標題式套語「一句話：」「核心理念：」「關鍵：」「以下是」。

**一看到就換**：

| 禁用 | 替代 |
|------|------|
| 賦能 | 讓⋯⋯能夠、給⋯⋯工具 |
| 深入探討 | 討論、分析、細看 |
| 揭示了 | 顯示、說明、指出 |
| 打造 | 做、建立、寫 |
| 旨在 | 為了、目的是 |
| 至關重要 / 不可或缺 | 重要、關鍵、必要（擇一，不疊加） |
| 進行 + 動詞 | 直接用動詞（「進行分析」→「分析」） |
| 在⋯⋯的過程中 / 在⋯⋯方面 | 拆框留核（「在重構的過程中」→「重構時」） |

**四個量化上限**：

1. 破折號（——）每千字至多一組。改成逗號或句號後語意不變，就改。  <!-- zhtw-lint: skip -->
2. 「不是 X，而是 Y」每千字至多一次，且要通過稻草人測試：真的有人會相信 X 嗎？沒有就直接說 Y。
3. 三項式排比（更 A、更 B、更 C）：三項可互相推導就砍到一項。
4. 加粗每段至多一處，整句加粗禁止。

**開場與收場**：不復述問題（「這是一個很好的問題」）、不用應答式熱情（「當然可以！」）、不用展望式收尾（「希望這些資訊對你有幫助」）。內容說完就停。

**贅詞「一個」**：英文冠詞的殘影，「一種」「一位」「一項」同理。刪掉後句子仍通就刪。

完整規則、例句與逐項自檢流程在 [prose-style.md](./references/prose-style.md)，寫連續散文時才需要讀。

## 品質檢查與重寫流程

速查表是給你第一次就寫對用的，不是事後對照用的。

1. 產出前掃一遍上方四塊（絕對禁用、軟體圈行話、一詞多義、AI 味速查），照著寫。
2. 查表。這步無條件執行，不看第 3 步的結果，而且候選詞不由你判斷。

   下面的路徑都相對於本 skill 目錄，不是相對於專案根目錄。

   能執行指令時，把草稿餵給腳本。用 stdin，不要另存暫存檔——存了就會忘記刪，skill 目錄裡會多出 `draft_check.txt` 這種殘骸：

   ```bash
   cat <<'EOF' | python3 scripts/lint_zhtw.py --terms -
   （草稿全文）
   EOF
   ```

   已經是檔案就直接給路徑：`python3 scripts/lint_zhtw.py --terms draft.md`。

   它逐列比對整份 terms.csv，不管你覺得哪個詞可疑。輸出格式是 `行號: [用詞] 原詞 → 建議`；標「（語境未確認）」表示該列有 `clues`，要自己確認語境對不對再改。

   只能 grep 時，pattern 要從草稿**機械地**抽：把每個連續中文字串按 2 到 6 字切出來全部放進去，不是放你覺得可疑的那幾個。

   ```bash
   grep -nE "候選1|候選2|候選3|…" references/terms.csv
   ```

   `cn` 欄同時收簡體與繁體兩種字形，兩種都要試。有命中就照 `tw` 欄改。

   為什麼候選詞不能自己挑：直覺只挑得出你已經知道有問題的詞。實測讓模型自行「挑出可疑的詞」，它挑的是本來就認得的那幾個，真正查了才會的詞一個都沒進 pattern，等於沒查。你覺得沒問題的詞，才是最需要查的那些。

   全篇一次餵完，不要逐段查、也不要每改一個詞就重跑一次。腳本一次讀整份草稿、一次列出所有命中列；命中清單看完一次全部改完，改完只需要照第 5 步再跑一次確認，不必每改一處就重新查一次。實測這樣拖到十幾次工具呼叫，慢，而且每一步都是可能斷掉的地方。
3. 產出後自我檢查一次，以下任一項成立即為不通過：
   - 出現「絕對禁用」或「中國軟體圈行話」表裡的詞
   - 一詞多義的詞用錯義項
   - 出現「AI 味速查」刪除清單或替換表裡的詞
   - 破折號、假對比、三項式排比、加粗超過量化上限（含整句加粗）
   - 開場復述問題，或收尾出現「希望這些資訊對你有幫助」
   - 中文句子用了半形標點，或程式碼與檔名沒加反引號
   - 英文專有名詞被翻譯掉（React、useState、API 要保留）
4. 通過：直接輸出，不要開啟 guidelines.md。
5. 未通過：讀 guidelines.md，重寫後再檢查一次。
6. 只輸出通過的版本，不要提及檢查或查表過程。

## Minimal Example

```markdown
使用 React，在 `useEffect()` 中載入資料。
檔案位於 `src/components/Button.tsx`。
```

## References

- [prose-style.md](./references/prose-style.md)：去 AI 味的完整行文規範（寫連續散文時讀）
- [guidelines.md](./references/guidelines.md)：完整指南（稽核時讀）
- [terms.csv](./references/terms.csv)：術語對照表，由 [scripts/fetch_terms.py](./scripts/fetch_terms.py) 產生
- 外部來源（Wikibooks、zhtw-mcp、教育部辭典）列在 guidelines.md
- [allenloves/de-ai-tone](https://github.com/allenloves/de-ai-tone)：CC BY-SA 4.0，`prose-style.md`、軟體圈行話表、一詞多義表的來源

**Last Updated**: 2026-08-09
