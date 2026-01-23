# Agent Skills

我的自訂 Claude Agent Skills 集合。這些技能擴展了 Copilot 的功能，提供專業知識與工作流程支援。

## 📚 Available Skills

### [Taiwan Traditional Chinese](./skills/taiwan-traditional-chinese)
**Taiwan zh_TW 繁體中文回應指南**

READ FIRST before ANY Traditional Chinese output (files, docs, markdown, comments, translations).

- ✅ 台灣繁體中文（zh_TW）術語標準
- ✅ 技術術語、標點、語氣規範
- ✅ 程式碼與框架名稱保留方案
- ✅ 完整術語對照表 (Wikibooks CC BY-SA 4.0)

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
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python references/fetch_terms.py
```

---

## 🚀 Installation

使用 `npx add-skill` 安裝技能。該工具會自動探索 `skills/` 目錄。

**列出可用技能：**
```bash
npx add-skill lanamaysu/agent-skills --list
```

**安裝特定技能：**
```bash
npx add-skill lanamaysu/agent-skills --skill taiwan-traditional-chinese
```

---

## 📖 Skill Structure

每個技能資料夾（在 `skills/` 下）包含：

- **SKILL.md** — 技能完整說明、使用時機、詳細規則
- **README.md** — 安裝、使用與維護指南
- **references/** — 參考資料、資料來源、授權資訊
- **rules/** — 具體規則與實踐範例

---

## 🔧 Development

### 建立新技能

每個技能應遵循統一結構：

```
skills/
  └── your-skill-name/
      ├── SKILL.md              # 技能定義與規則
      ├── README.md             # 安裝與使用指南
      ├── requirements.txt      # 依賴（若有）
      └── references/           # 參考資料與來源
          ├── README.md
          └── *.csv / *.md
```

---

## 📝 License

本 repository 採用 MIT License，但個別技能可能包含不同授權的參考資料。

- **技能內容**：MIT License
- **參考資料**：依各技能 references 資料夾說明（如 taiwan-traditional-chinese/references/terms.csv 採用 CC BY-SA 4.0）

詳見各技能資料夾的 README 與 references 說明。

---

**Last Updated:** 2026-01-23
