# orca-plugins (Orca 外掛 Monorepo)

這是由 **[fuevaco](https://github.com/fuevaco)** 維護的 [Orca](https://github.com/stablyai/orca) 外掛合集儲存庫。本專案採用最新版 Orca 官方規格的 **Monorepo** 架構與 **`orca-catalog.json` (Catalog v2)**，支援在同一個來源儲存庫中獨立維護、發布多個不同的外掛套件。

> [!WARNING]
> **使用須知與免責提示**：
> 本儲存庫套件主要為作者**個人自用與日常開發**維護，更新頻率視個人需求而定。使用本套件所產生之任何相容性問題或風險，均需由**使用者自行承擔**。詳見 [免責聲明](#免責聲明-disclaimer)。

## 免責聲明 (Disclaimer)

使用或安裝本儲存庫任何外掛即代表您瞭解並同意以下條款：

1. **個人自用性質**：本專案為個人業餘維護與實驗性質，雖然維護者會盡力保持外掛完整性與安全性，但**不保證**所有套件均完全無誤，亦不保證與 Orca 所有版本或第三方擴充功能完全相容。
2. **依「現狀（AS-IS）」提供**：本專案依現狀提供，不包含任何明示或暗示的保證（包括但不限於適用性、穩定性、商業可用性或特定目的之適用性）。
3. **風險自負**：因安裝、載入或使用本儲存庫套件而導致之任何直接、間接、附帶或衍生性損失（包含但不限於介面顯示錯位、外掛載入失敗、操作錯誤等），**均由使用者自行承擔全責**，維護者概不承擔任何法律與賠償責任。
4. **非官方產品**：本儲存庫為社群獨立維護，**並非** Stably AI 或 Orca 官方出品，亦未獲官方背書或授權。
5. **維護與更新義務**：Orca 官方版本更新頻繁，維護者保留隨時修改、暫停或終止本專案更新之權利，不承擔即時同步官方更新之義務。
6. **不開放社群回饋與技術支援**：本儲存庫純屬個人開發存檔與自用，**無意經營開源社群，亦不接受任何 Issue 回報、功能請求或 Pull Request（PR）**。相關回饋概不受理。

---

## 本儲存庫收錄套件 (Packages)

| 套件 ID | 目錄路徑 | 類型 | 說明 |
| :--- | :--- | :--- | :--- |
| **`fuevaco.zh-tw`** | [`plugins/zh-tw`](./plugins/zh-tw) | `interface-language` | Orca 繁體中文（台灣，zh-TW）介面語言套件 |

---

## 使用者安裝方式 (Installation)

在 Orca 中只需新增一次來源，即可自由選擇安裝本儲存庫的任一套件：

1. 開啟 Orca，前往 **Settings → Plugins → Marketplace Sources**（或 Manage Sources）。
2. 點選 **Add Source**，新增來源：
   - **URL**: `https://github.com/fuevaco/orca-tw.git`
   - **Ref / Branch**: `main`
3. 新增後，Orca 會自動讀取根目錄的 `orca-catalog.json`，並在列表或 Marketplace 中顯示本儲存庫包含的所有外掛。
4. 點選欲安裝的外掛（如 **繁體中文 (台灣)**）後按下 **Install** 即可。

> [!NOTE]
> 本機開發模式：亦可在 **Settings → Plugins → Local Development** 中直接將路徑指向特定的子目錄（如 `plugins/zh-tw`）。

---

## Monorepo 開發與維護指南 (For Maintainer)

### 1. 目錄結構
```text
orca-tw/
├── orca-catalog.json           <-- 最新版 v2 目錄索引檔（由 scripts/generate_catalog.mjs 自動產生）
├── orca-marketplace.json       <-- 舊版相容檔案
├── scripts/
│   ├── create_plugin.mjs       <-- 快速建立新套件骨架工具
│   ├── generate_catalog.mjs    <-- 自動掃描 plugins/ 並更新 orca-catalog.json
│   └── update_translations.py  <-- 繁體中文字典自動同步工具
└── plugins/
    ├── zh-tw/                  <-- 繁體中文語言套件
    │   ├── orca-plugin.json
    │   ├── README.md
    │   └── locales/
    └── <未來新增的套件>/
        ├── orca-plugin.json
        └── README.md
```

### 2. 新增一個新外掛套件
在專案根目錄執行：
```bash
node scripts/create_plugin.mjs <套件ID> "<套件名稱>" [類型]
```
例如：
```bash
# 建立一個新主題套件
node scripts/create_plugin.mjs custom-dark "極簡深色主題" theme

# 建立一個自訂指令套件
node scripts/create_plugin.mjs dev-shortcuts "開發常用快捷指令" declarative
```

### 3. 自動更新市場目錄索引
每當新增套件或修改現有套件後，只需執行：
```bash
node scripts/generate_catalog.mjs
```
指令會自動：
- 遍歷 `plugins/` 底下所有的外掛目錄。
- 讀取各套件的 `orca-plugin.json`。
- 自動計算該目錄的 SHA-256 內容雜湊（`contentHash`）。
- 自動生成最新符合規範的 `orca-catalog.json`！

---

## 無社群支援政策

本專案純屬個人自用存檔，**無意經營開源社群，亦不接受任何 Issue 回報或 Pull Request（PR）**。
若有客製化需求，請直接 **Fork** 本儲存庫並依照個人需要修改使用。
