# Agent Skills

我的自訂 Claude Agent Skills 集合，為 Claude Code 補上領域知識與工作流程規範。

## Available Skills

### [Taiwan Traditional Chinese](./skills/taiwan-traditional-chinese)
**Taiwan zh-Hant-TW/zh-TW/zh_TW 繁體中文回應指南**

先做品質檢查，僅在不通過時才讀取完整指南與術語對照表。

- 台灣繁體中文（zh-Hant-TW/zh-TW/zh_TW）術語標準
- 技術術語、標點、語氣規範
- 程式碼與框架名稱保留方案
- 完整術語對照表（Wikibooks CC BY-SA 4.0）

**使用時機：**
- 撰寫或審查中文文件、程式碼註解、提交訊息
- 需要統一台灣技術術語與格式風格
- 任何繁體中文內容生成任務

**快速開始：**
```bash
# 預覽技能
cat skills/taiwan-traditional-chinese/SKILL.md

# 更新術語對照表
cd skills/taiwan-traditional-chinese
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/fetch_terms.py
```

---

### [Jest + React Testing Library](./skills/jest-rtl-testing)
**Jest + RTL 測試最佳實踐**

基於 Testing Library 核心原則與 Kent C. Dodds 最佳實踐的測試指南。

- 以使用者為中心的測試方法
- Query 優先順序指南（accessibility-first）
- 常見錯誤與正確做法對照
- 非同步測試處理模式
- 優先讀取專案 AGENTS.md 的測試規範

**使用時機：**
- 撰寫或審查 React component 測試
- 測試失敗時除錯，判斷 API 使用是否正確
- 需要改善測試可讀性與可維護性
- 確保測試遵循無障礙（accessibility）最佳實踐

**快速開始：**
```bash
# 預覽技能
cat skills/jest-rtl-testing/SKILL.md

# 查看 Query 速查表
cat skills/jest-rtl-testing/references/query-cheatsheet.md

# 查看常見測試模式
cat skills/jest-rtl-testing/references/common-patterns.md
```

---

## Installation

使用 `npx add-skill` 安裝技能。該工具會自動探索 `skills/` 目錄。

**列出可用技能：**
```bash
npx add-skill lanamaysu/agent-skills --list
```

**安裝特定技能：**
```bash
# 安裝台灣繁體中文技能
npx add-skill lanamaysu/agent-skills --skill taiwan-traditional-chinese

# 安裝 Jest + RTL 測試技能
npx add-skill lanamaysu/agent-skills --skill jest-rtl-testing
```

---

## Skill Structure

每個技能資料夾（在 `skills/` 下）包含：

- **SKILL.md** — 技能完整說明、使用時機、詳細規則
- **README.md** — 安裝、使用與維護指南
- **references/** — 按需載入的參考資料、資料來源、授權資訊
- **scripts/** — 維護工具（選用）

---

## Development

### 建立新技能

每個技能應遵循統一結構：

```
skills/
  └── your-skill-name/
      ├── SKILL.md              # 技能定義與規則
      ├── README.md             # 安裝與使用指南
      └── references/           # 參考資料與來源
          ├── README.md
          └── *.csv / *.md
```

需要維護腳本時再加 `scripts/`，把 `requirements.txt` 放在該資料夾內。

---

## License

本 repository 採用 MIT License，但個別技能可能不同：技能資料夾內若有 `LICENSE`，以該檔為準。

| 範圍 | 授權 |
|------|------|
| repository 與未特別標示的技能 | MIT License |
| `skills/taiwan-traditional-chinese/` | **CC BY-SA 4.0**（見該資料夾的 `LICENSE`） |

`taiwan-traditional-chinese` 之所以不同：它含有 CC BY-SA 4.0 素材的改作（Wikibooks 術語對照表、[allenloves/de-ai-tone](https://github.com/allenloves/de-ai-tone) 的行文規範）。ShareAlike 條款要求改作本以相同或相容授權散佈，而 MIT 與 BY-SA 不相容。若你要再散佈該資料夾或其改作，請保留出處並同樣以 CC BY-SA 4.0 釋出。

詳見各技能資料夾的 `LICENSE` 與 README。

---

**Last Updated**: 2026-07-31
