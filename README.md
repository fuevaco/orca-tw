# orca-tw (Orca 繁體中文語言套件)

[Orca](https://github.com/stablyai/orca) 繁體中文（台灣，zh-TW）語言套件。

## 狀態與涵蓋範圍

本語言套件目前收錄超過 **13,400 條字串**，全面涵蓋：
- 設定（Settings）與外掛管理
- 側邊欄（Sidebar）與工作區（Workspace / Worktree）管理
- 編輯器（Editor）與內建終端機（Terminal）
- GitHub / GitLab / Linear / Jira 等服務整合
- Agent 代理對話、執行階段（Runtime）與自動化工作流程
- 行動端小幫手、控制面板、系統匣與應用程式選單

尚未翻譯的新增字串會自動回退（Fallback）至 Orca 內建的英文翻譯。

## 安裝方式

Orca 透過其外掛系統（Plugin System）探索語言套件：

1. 開啟 Orca，在設定中的外掛（Plugins）新增來源，指向本儲存庫或本地目錄路徑（例如 `F:\orca-tw`）。
2. 在 **Settings → Appearance → Language** 中選擇 **繁體中文 (台灣) — orca-tw**。
3. 重新啟動或重新整理介面以套用繁體中文。

## 語言套件建置原則

本套件基於 Orca 官方語言目錄進行台灣繁體中文本地化，遵循以下規範：

1. **符合台灣軟體工程慣用語**：
   - `Workspace` → **工作區**、`Worktree` → **工作樹**
   - `Repository` → **儲存庫**、`Branch` → **分支**、`Commit` → **提交**
   - `Project` → **專案**、`Tab` → **分頁**、`Terminal` → **終端機**
   - `Plugin` → **外掛**、`Settings` → **設定**、`Default` → **預設**
   - `Memory` → **記憶體**、`Cache` → **快取**、`Server` → **伺服器**
   - `Duplicate` → **建立副本**、`Copy` → **複製**、`Stage` → **暫存**
2. **完整保護變數插值與指令**：
   - 嚴格保留所有 `{{value0}}`、`{{endpoint}}`、`{{branch}}` 等插值佔位符。
   - 保留 CLI 指令、參數及專有名詞（如 `--model sonnet`、`pnpm install`、`orca.yaml`、`/goal`、`origin`、`Ghostty`、`Antigravity`、`Claude`、`Codex`、`Gemini` 等）。
3. **符合 Orca 外掛安全與載入規範**：
   - 通過 `parsePluginLanguagePackArtifact` 嚴格檢驗：符合最大巢狀深度（<= 16）、最大條目數（<= 20,000）、排除設定安全保護鍵（`auto.components.settings.Plugin*`）及超長行內樣式，確保外掛載入零錯誤。

## 貢獻指南

歡迎提供勘誤與翻譯改善建議！歡迎針對 `locales/zh-TW.json` 提交 PR 或 Issue。

