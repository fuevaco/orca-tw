# orca-tw (Orca 繁體中文語言套件)

[Orca](https://github.com/stablyai/orca) 繁體中文（台灣，zh-TW）語言套件，由 **[fuevaco](https://github.com/fuevaco)** 維護。

> [!WARNING]
> **使用須知與免責提示**：
> 本套件主要為作者**個人自用與日常開發**維護，翻譯與更新頻率視個人需求而定。使用本套件所產生之任何相容性問題或風險，均需由**使用者自行承擔**。詳見 [免責聲明](#免責聲明-disclaimer)。

## 免責聲明 (Disclaimer)

使用或安裝本語言套件即代表您瞭解並同意以下條款：

1. **個人自用性質**：本專案為個人業餘維護與實驗性質，雖然維護者會盡力保持字串完整性與安全性，但**不保證**所有翻譯均完全正確無誤，亦不保證與 Orca 所有版本或第三方擴充功能完全相容。
2. **依「現狀（AS-IS）」提供**：本專案依現狀提供，不包含任何明示或暗示的保證（包括但不限於適用性、穩定性、商業可用性或特定目的之適用性）。
3. **風險自負**：因安裝、載入或使用本語言套件而導致之任何直接、間接、附帶或衍生性損失（包含但不限於介面顯示錯位、外掛載入失敗、語義理解偏差引發之操作錯誤等），**均由使用者自行承擔全責**，維護者概不承擔任何法律與賠償責任。
4. **非官方產品**：本語言套件為社群獨立維護，**並非** Stably AI 或 Orca 官方出品，亦未獲官方背書或授權。
5. **維護與更新義務**：Orca 官方版本更新頻繁，維護者保留隨時修改、暫停或終止本專案更新之權利，不承擔即時同步官方更新之義務。
6. **不開放社群回饋與技術支援**：本儲存庫純屬個人開發存檔與自用，**無意經營開源社群，亦不接受任何 Issue 回報、功能請求或 Pull Request（PR）**。相關回饋概不受理。

## 狀態與涵蓋範圍

本語言套件收錄超過 **17,000 條字串**（共 17,066 條可翻譯字串，19,179 條外掛結構條目），全面涵蓋：
- 設定（Settings）與外掛管理
- 側邊欄（Sidebar）與工作區（Workspace / Worktree）管理
- 編輯器（Editor）與內建終端機（Terminal）
- GitHub / GitLab / Linear / Jira 等服務整合
- Agent 對話、執行環境（Runtime）與自動化工作流程
- 行動版小幫手、控制面板、系統匣與應用程式選單

尚未翻譯的新增字串會自動回退（Fallback）至 Orca 內建的英文翻譯。

## 安裝方式

Orca 透過其外掛系統（Plugin System）探索語言套件：

1. 開啟 Orca，在 **Settings → Plugins** 中安裝本外掛（可選擇 Local folder 指向本專案目錄，或輸入 Git URL `https://github.com/fuevaco/orca-tw.git#main`）。
2. 在 **Settings → Appearance → Language** 中選擇 **繁體中文 (台灣) — fuevaco.zh-tw**。
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

## 無社群支援與貢獻政策

本專案純屬個人自用存檔，**無意經營開源社群，亦不接受任何 Issue 回報或 Pull Request（PR）**。

若您在使用過程中有任何翻譯微調或客製化需求，請直接 **Fork** 本儲存庫並依照個人需要修改使用。
