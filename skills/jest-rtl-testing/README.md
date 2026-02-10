# Jest + React Testing Library 測試最佳實踐

協助撰寫以使用者為中心的 React 測試的技能指南。

## 概述

本技能基於 Testing Library 的核心原則與 Kent C. Dodds 的最佳實踐建議，提供：
- Query 優先順序指南（情境化）
- 常見錯誤與正確做法對照
- 非同步測試處理模式
- 專案特定規範整合（優先讀取 AGENTS.md）

## 核心特色

✅ **專案規範優先** - 優先遵循 `AGENTS.md` 規則，本技能作為補充指引  
✅ **情境化 Query 優先順序** - 根據元件大小選擇最佳 query 方法  
✅ **MSW 強烈推薦** - 網路層級的 API mocking，不綁定實作細節  
✅ **效能考量** - 警告 `getByRole` 在大型 view 的效能問題  
✅ **常見錯誤對照** - 錯誤做法 vs 正確做法的對比範例  
✅ **非同步處理** - findBy、waitFor、waitForElementToBeRemoved 使用時機  
✅ **使用者互動** - userEvent vs fireEvent 的差異與建議  
✅ **除錯指南** - 測試失敗時的系統化除錯步驟

## 安裝

```bash
npx add-skill lanamaysu/agent-skills --skill jest-rtl-testing
```

或列出所有可用技能：

```bash
npx add-skill lanamaysu/agent-skills --list
```

## 使用時機

- 撰寫新的 Jest + React Testing Library 測試
- 審查或重構現有測試程式碼
- 測試失敗時除錯，需判斷 API 使用是否正確
- 需要優化測試可讀性與可維護性
- 確保測試遵循無障礙（accessibility）最佳實踐

## 快速參考

### Query 優先順序（情境化）

- **小型元件**：優先 `getByRole`（無障礙驗證）
- **大型 View**：優先 `getByLabelText` / `getByText`（效能較佳）
- **最後手段**：`getByTestId`（請說明原因）

完整說明請見 [references/query-cheatsheet.md](./references/query-cheatsheet.md)。

### 專案規範

- 先讀 `AGENTS.md` 的 Testing 規範
- 專案規範優先，本技能作為補充

更多範例與模式請見 [SKILL.md](./SKILL.md) 與 [references/common-patterns.md](./references/common-patterns.md)。

## 技能結構

```
jest-rtl-testing/
├── SKILL.md              # 完整技能指南
├── README.md             # 本檔案
└── references/
    ├── README.md         # 參考資料說明
    ├── query-cheatsheet.md    # Query 速查表
    └── common-patterns.md     # 常見測試模式
```

## 延伸資源

### 官方文件
- [Testing Library - Guiding Principles](https://testing-library.com/docs/guiding-principles)
- [Testing Library - Queries](https://testing-library.com/docs/queries/about)
- [Testing Library - Async Utilities](https://testing-library.com/docs/dom-testing-library/api-async)
- [user-event Documentation](https://testing-library.com/docs/user-event/intro)
- [MSW Documentation](https://mswjs.io/docs/)

### 推薦閱讀
- [Common mistakes with React Testing Library - Kent C. Dodds](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
- [Testing Implementation Details](https://kentcdodds.com/blog/testing-implementation-details)
- [Making your UI tests resilient to change](https://kentcdodds.com/blog/making-your-ui-tests-resilient-to-change)
- [getByRole Performance Issue](https://github.com/testing-library/dom-testing-library/issues/820)

## 授權

MIT License

---

**Last Updated**: 2026-02-10
