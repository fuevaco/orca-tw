import json
import os
import re
import sys
import opencc

sys.stdout.reconfigure(encoding='utf-8')

UPSTREAM_EN = r"C:\Users\genius\AppData\Local\Temp\orca-upstream\src\renderer\src\i18n\locales\en.json"
UPSTREAM_ZH = r"C:\Users\genius\AppData\Local\Temp\orca-upstream\src\renderer\src\i18n\locales\zh.json"
CURRENT_ZH_TW = r"F:\Orca_繁中語言套件\locales\zh-TW.json"
OUTPUT_ZH_TW = r"F:\Orca_繁中語言套件\locales\zh-TW.json"

TRANSLATABLE_PLUGIN_CHROME = {
    'auto.components.settings.PluginsSettingsSection.title',
    'auto.components.settings.PluginsSettingsSection.systemLabel',
    'auto.components.settings.PluginsSettingsSection.install',
    'auto.components.settings.PluginsSettingsSection.loading',
    'auto.components.settings.PluginsSettingsSection.empty',
    'auto.components.settings.PluginsSettingsSection.emptyTitle',
    'auto.components.settings.PluginsSettingsSection.noInstalledResults',
    'auto.components.settings.PluginsSettingsSection.noInstalledResultsTitle',
    'auto.components.settings.PluginMarketplaceBrowser.manageSources',
    'auto.components.settings.PluginMarketplaceBrowser.addSource',
    'auto.components.settings.PluginMarketplaceBrowser.refresh',
    'auto.components.settings.PluginMarketplaceBrowser.refreshing',
    'auto.components.settings.PluginMarketplaceBrowser.loading',
    'auto.components.settings.PluginMarketplaceBrowser.tryAgain',
    'auto.components.settings.PluginMarketplaceBrowser.clearSearch',
    'auto.components.settings.PluginMarketplaceBrowser.empty',
    'auto.components.settings.PluginMarketplaceBrowser.emptyTitle',
    'auto.components.settings.PluginMarketplaceBrowser.noInstalled',
    'auto.components.settings.PluginMarketplaceBrowser.noInstalledTitle',
    'auto.components.settings.PluginMarketplaceBrowser.noResults',
    'auto.components.settings.PluginMarketplaceBrowser.noResultsTitle',
    'auto.components.settings.PluginMarketplaceBrowser.noSourcesTitle',
    'auto.components.settings.PluginDevelopmentSection.title',
    'auto.components.settings.PluginDevelopmentSection.add',
    'auto.components.settings.PluginDevelopmentSection.remove',
    'auto.components.settings.PluginDevelopmentSection.pathLabel',
    'auto.components.settings.PluginDevelopmentSection.pathRequired',
    'auto.components.settings.PluginDevelopmentSection.placeholder',
    'auto.components.settings.plugins.search.title',
    'auto.components.settings.plugins.search.description',
    'auto.components.settings.plugins.search.install',
    'auto.components.settings.plugins.search.permissions',
    'auto.components.settings.plugins.search.logs',
    'auto.components.settings.plugins.search.development'
}

TRANSLATABLE_CONTAINERS = set()
for p in TRANSLATABLE_PLUGIN_CHROME:
    parts = p.split('.')
    for i in range(1, len(parts)):
        TRANSLATABLE_CONTAINERS.add('.'.join(parts[:i]))

PROTECTED_ROOT = 'auto.components.settings.'
PROTECTED_RE = re.compile(r'^plugin', re.IGNORECASE)

def is_protected_path(path):
    if not path.startswith(PROTECTED_ROOT):
        return False
    if path in TRANSLATABLE_PLUGIN_CHROME:
        return False
    return bool(PROTECTED_RE.search(path[len(PROTECTED_ROOT):]))

def is_container_path(path):
    return path in TRANSLATABLE_CONTAINERS

MANUAL_TRANSLATIONS = {
    # Browser history
    "browser.history.clear": "清除瀏覽紀錄",
    "browser.history.clearAllTime": "不限時間",
    "browser.history.clearLastHour": "過去 1 小時",
    "browser.history.clearRange": "清除此時間範圍的歷史紀錄：",
    "browser.history.clearToday": "今天",
    "browser.history.cleared": "已清除瀏覽紀錄",
    "browser.history.close": "關閉",
    "browser.history.description": "搜尋並管理瀏覽紀錄",
    "browser.history.empty": "您造訪過的頁面將顯示於此",
    "browser.history.enterKey": "Enter",
    "browser.history.escKey": "Esc",
    "browser.history.menuItem": "歷史紀錄",
    "browser.history.noMatches": "沒有符合您搜尋條件的頁面",
    "browser.history.open": "開啟",
    "browser.history.remove": "從歷史紀錄中移除",
    "browser.history.removeShort": "移除",
    "browser.history.search": "搜尋歷史紀錄",
    "browser.history.title": "歷史紀錄",
    "browser.history.today": "今天",
    "browser.history.yesterday": "昨天",

    # Editor
    "editor.fileLoad.remoteTooLarge": "此檔案過大，無法從其主機開啟。",

    # Settings: Chat & Appearance
    "settings.chat.permissionsDescriptionOwnAgents": "新聊天將遵循「設定 → Agent」中各 Agent 的權限。",
    "settings.appearance.chat.fontKeywordTypeface": "字型",
    "settings.appearance.chat.fontKeywordTypography": "字型排版",

    # Settings: Agents
    "settings.agents.permissionsTitle": "權限",
    "settings.agents.permissionsChoiceExplanation": "所有 Agent 在不主動詢問下可執行的動作。您可以在下方針對特定 Agent 進行個別設定。",
    "settings.agents.permissionEachOwn": "各 Agent 自身的設定",
    "settings.agents.permissionEachOwnDescription": "Orca 不額外附加參數；各 CLI 使用自身配置",
    "settings.agents.permissionArgsTerminalOnly": "這些引數可能會控制 {{agent}} 的終端機權限，因此 Orca 不額外附加參數旗標。聊天將使用上方的「權限」設定。",
    "settings.agents.localSaveFailed": "無法儲存 Agent 設定。請重試。",
    "settings.agents.localSaveFailedAgent": "無法儲存 {{agent}} 的設定。請重試。",
    "settings.agents.permissionFromArgs": "終端機與新聊天中的 {{agent}} 已設為 {{mode}}。",
    "settings.agents.permissionFromArgsTerminals": "終端機中的 {{agent}} 已設為 {{mode}}。",
    "settings.agents.permissionOwnAgent": "使用 {{agent}} 自身的設定",
    "settings.agents.permissionOwnAll": "Agent 自身的設定",
    "settings.agents.permissionOwnLegacyDescription": "Orca 在終端機中不附加權限旗標；聊天將使用「設定 → 聊天」。",
    "settings.agents.permissionOwnDescription": "終端機與聊天遵循該 Agent 自身的權限設定。",
    "settings.agents.permissionChoiceDescription": "套用於支援此模式的各 Agent。可在下方變更個別 Agent。",
    "settings.agents.permissionOwnShort": "自身設定",
    "settings.agents.permissionWithoutAuto": "不具備「為我核准」權限的 Agent",
    "settings.agents.permissionSurfaceDifference": "終端機使用 Agent 自身的設定；新聊天使用 {{mode}}。",
    "settings.agents.permissionSameAsAll": "與所有 Agent 相同",
    "settings.agents.permissionChipRemove": "移除 {{flag}} 並使用 {{agent}} 自身的設定",
    "settings.agents.permissionChipTooltip": "由「權限」所新增。將其移除以使用 {{agent}} 自身的設定。",
    "settings.agents.permissionOverridesKept": "{{count}} 個 Agent 仍使用其自身權限設定：",
    "settings.agents.permissionOverridesKept_one": "{{count}} 個 Agent 仍使用其自身權限設定：",
    "settings.agents.permissionOverridesKept_other": "{{count}} 個 Agent 仍使用其自身權限設定：",
    "settings.agents.permissionOverridesFollow": "{{count}} 個 Agent 現已遵循 {{mode}}",
    "settings.agents.permissionOverridesFollow_one": "{{count}} 個 Agent 現已遵循 {{mode}}",
    "settings.agents.permissionOverridesFollow_other": "{{count}} 個 Agent 現已遵循 {{mode}}",
    "settings.agents.permissionOverrideFollows": "{{agent}} 現已遵循 {{mode}}",
    "settings.agents.permissionOverrideMore": "以及其他 {{count}} 個",
    "settings.agents.permissionOverrideMore_one": "以及其他 {{count}} 個",
    "settings.agents.permissionOverrideMore_other": "以及其他 {{count}} 個",
    "settings.agents.permissionOverridesUse": "使用 {{mode}}",
    "settings.sourceControl.actionPermissions.sameAsAgent": "與 {{agent}} 相同",

    # Worktrees & git
    "auto.store.slices.worktrees.localBaseRefShallowHistoryTitle": "未更新本機 {{value0}}：淺層複製（Shallow Clone）",
    "auto.store.slices.worktrees.localBaseRefShallowHistoryNamed": "\"{{value0}}\" 建立自 {{value1}} 且不受影響。Orca 無法同時更新您的本機 {{value2}} 分支，因為此複製品僅包含近期的歷程記錄，Git 無法確認本機 {{value2}} 是否僅落後於遠端。若要為日後所有新工作區修正此問題，請執行一次：",
    "auto.store.slices.worktrees.localBaseRefShallowHistory": "您的工作區建立自 {{value0}} 且不受影響。Orca 無法同時更新您的本機 {{value1}} 分支，因為此複製品僅包含近期的歷程記錄，Git 無法確認本機 {{value1}} 是否僅落後於遠端。若要為日後所有新工作區修正此問題，請執行一次：",
    "auto.store.slices.worktrees.localBaseRefRefreshTurnOff": "停用檢查",
    "auto.store.slices.worktrees.localBaseRefRefreshTurnOffHelp": "停用檢查的作用說明",
    "auto.store.slices.worktrees.localBaseRefRefreshTurnOffTooltip": "關閉 Orca 設定 {{value0}}。當您建立工作區時，Orca 將停止更新本機 {{value1}}，且此警告將不再出現。新工作區不受影響。您可以隨時在「設定 › Git」中重新開啟此功能。",
    "auto.store.slices.worktrees.localBaseRefUnshallow": "完整擷取（Unshallow）",
    "auto.store.slices.worktrees.localBaseRefUnshallowFailed": "無法為此工作區開啟終端機",
    "auto.store.slices.worktrees.localBaseRefUnshallowFailedDescription": "請改為在此儲存庫的終端機中執行 {{value0}}。",
    "auto.store.slices.worktrees.localBaseRefRefreshTurnedOff": "Orca 將不再更新本機 {{value0}}",
    "auto.store.slices.worktrees.localBaseRefRefreshTurnedOffDescription": "可在「設定 › {{value0}}」中重新開啟。",
    "auto.store.slices.worktrees.localBaseRefRefreshTurnOffFailed": "無法關閉 {{value0}}",

    # Cookie & drop failure
    "auto.lib.browser.cookie.import.toast.secretToolMissing": "由於未安裝 secret-tool，Orca 無法讀取 {{browser}} 的 {{count}} 個加密 Cookie。請安裝 libsecret-tools（或您發行版的對應套件）後再次匯入。",
    "auto.lib.browser.cookie.import.toast.cookieKeyLocked": "由於系統金鑰圈（Keyring）存取被鎖定或拒絕，Orca 無法讀取 {{browser}} 的 {{count}} 個加密 Cookie。請解鎖登入金鑰圈，若出現提示請允許存取，然後再次匯入。",
    "auto.lib.browser.cookie.import.toast.cookieKeyUnavailable": "由於無法讀取 Cookie 加密金鑰，Orca 無法讀取 {{browser}} 的 {{count}} 個加密 Cookie。請嘗試再次匯入、使用「從檔案…」匯入 Cookie，或直接在 Orca 中登入。",
    "auto.lib.browser.cookie.import.toast.otherUndecryptableCookies": "還有 {{count}} 個 Cookie 因其他原因無法解密。",
    "auto.lib.dropFailureReason.tooLarge": "檔案過大，無法上傳至此主機。",
    "auto.lib.dropFailureReason.noSpace": "主機磁碟空間不足。",
    "auto.lib.dropFailureReason.changed": "檔案在上傳過程中已被修改。請重試。",
    "auto.lib.dropFailureReason.hostUnreachable": "與主機的連線發生變更或中斷。請重試。",
    "auto.lib.dropFailureReason.disconnected": "主機已中斷連線。",
    "auto.lib.dropFailureReason.unknownOne": "無法上傳此檔案。",
    "auto.lib.dropFailureReason.unknownMany": "無法上傳這些檔案。",
    "auto.lib.aiVaultResumeRefusal.preparationRefused": "Orca 無法準備此 {{value0}} 對話。請開啟新聊天以繼續。",
    "auto.lib.claudeAgentRowView.restartRequired": "在此窗格中重新啟動 Claude 以啟用子 Agent（Subagent）導覽。需使用支援 Orca 勾點（Hook）的較新版本 Claude。",
    "auto.lib.claudeAgentRowView.permissionPrompt": "切換 Agent 之前，請先回應 Claude 的權限提示。",
    "auto.lib.claudeAgentRowView.agentUnavailable": "Claude 無法開啟此 Agent。該 Agent 可能已不再可用。",
    "auto.lib.claudeAgentRowView.closeDialog": "Claude 未能切換檢視。請關閉所有開啟的對話方塊後重試。",
    "auto.lib.claudeAgentRowView.hostUnavailable": "此主機無法使用子 Agent 導覽。請更新 Orca 並在此窗格中重新啟動 Claude。",
    "auto.hooks.useGlobalFileDrop.hostMismatch": "此編輯器位於不同的主機上。請從檔案所屬的來源工作區中開啟它。",
    "auto.hooks.useGlobalFileDrop.workspaceOpenFailed": "無法開啟 {{fileName}}。請從其來源工作區開啟並重試。",

    # NativeChat & components
    "auto.components.NativeChatResumeOnRestartModal.serverTitle": "{{machine}} 已重新啟動",
    "auto.components.NativeChatResumeOnRestartModal.serverBody": "在 {{machine}} 上的 Orca 重新啟動時，這些聊天正在進行中。恢復執行將還原各聊天至中斷時的狀態，並要求 Agent 繼續執行。不會重複傳送您的原始提示詞。",
    "auto.components.NativeChatResumeOnRestartModal.serverDismiss": "略過",
    "auto.components.NativeChatResumeOnRestartModal.serverResumeAll": "恢復執行 {{machine}} 上的全部 {{count}} 個聊天",
    "auto.components.NativeChatResumeOnRestartModal.serverResumeHereOne": "恢復執行在此處啟動的 1 個聊天",
    "auto.components.NativeChatResumeOnRestartModal.serverResumeHere": "恢復執行在此處啟動的 {{count}} 個聊天",
    "auto.components.Terminal.reloadSnapshotSaveFailed": "重新載入已取消：無法儲存工作階段快照（{{value0}}）。",
    "auto.components.github.pr.merge.state.def355ff38": "可進行合併",
    "auto.components.github.pr.merge.state.e42c5bae67": "GitHub 顯示此 PR 可合併且檢查已通過",
    "auto.components.github.pr.merge.state.cbf0113af6": "GitHub 顯示此 PR 可合併",
    "auto.components.tab.bar.QuickLaunchButton.terminalListNeedsServerUpdate": "請更新此伺服器上的 Orca 以列出終端機 Agent",
    "auto.components.tab.bar.QuickLaunchButton.terminalListFailed": "無法列出此工作區的終端機 Agent",
    "auto.components.status.bar.StatusBar.4025a6f62f": "無限制",
    "auto.components.status.bar.StatusBar.a95969101f": "{{value0}} 點額度",
    "auto.components.status.bar.provider.extra.usage.section.apiKeyBalanceUnavailable": "此用量回應中未包含餘額。",
    "auto.components.status.bar.tooltip.fbc80d8be2": "Zen 餘額",
    "auto.components.status.bar.tooltip.c03c61f53f": "餘額",
    "auto.components.status.bar.tooltip.f6a27a3c0a": "可用 {{value0}}",
    "auto.components.status.bar.tooltip.7404abbece": "使用額度",
    "auto.components.status.bar.tooltip.473d45cd0f": "餘額 {{value0}}",
    "auto.components.status.bar.tooltip.f21b2ba897": "額度",
    "auto.components.status.bar.tooltip.56c0d70577": "無限制",
    "auto.components.status.bar.tooltip.87b5bda4d3": "可用額度：{{value0}} 點",
    "auto.components.sidebar.wslHostRowStatus.removalPending": "移除尚未完成",
    "auto.components.sidebar.wslHostRemoval.pending": "Orca 尚未移除主機：{{value0}} 再次點選移除以重試，或重新連線以保留。",
    "auto.components.settings.AccountsPane.opencodeGo.apiKey.checking": "正在檢查…",
    "auto.components.settings.AccountsPane.opencodeGo.apiKey.unavailable": "狀態無法取得",
    "auto.components.settings.SshTargetForm.proxyConnectionReuse": "重複使用單一 Proxy 連線",
    "auto.components.settings.SshTargetForm.proxyConnectionReuseHelp": "透過較慢的 ProxyCommand 或 ProxyJump 主機加速連線。僅在您的 ssh_config 未依賴主機專屬的 Match 或 %h 規則時啟用。",
    "auto.components.settings.SourceControlActionRepoOverrideNote.surface": "聊天或 CLI",
    "auto.components.settings.sshHostServer.automationsLeftDisabled_one": "此主機上的 Orca 伺服器已接管 {{count}} 個自動化工作流程，但無法將其重新開啟。請在「自動化」中手動開啟。",
    "auto.components.settings.sshHostServer.automationsLeftDisabled_other": "此主機上的 Orca 伺服器已接管 {{count}} 個自動化工作流程，但無法將其重新開啟。請在「自動化」中手動開啟。",
    "auto.components.settings.sshHostServer.windowsBuildUnsupported": "此主機執行的 Windows 版本舊於 Windows 10 與 Windows Server 2016，無法執行 Orca 伺服器。請使用較新版本的 Windows 主機，或改用 Linux 或 macOS 主機。",
    "auto.components.settings.sshHostServer.windowsNoExtractor": "此 Windows 主機既無 tar.exe 也無 PowerShell 的 Expand-Archive，導致 Orca 無法在此解壓縮其伺服器。請在該主機上安裝 Windows PowerShell 5.1，然後再次連線。",
    "auto.components.settings.sshHostServer.automationsLeftDisabled": "此主機上的 Orca 伺服器已接管 {{count}} 個自動化工作流程，但無法將其重新開啟。請在「自動化」中手動開啟。",
    "auto.components.settings.recoverServer.title": "復原 Orca 伺服器",
    "auto.components.settings.recoverServer.description": "由於先前執行留下的鎖定檔仍存在，此主機上的 Orca 伺服器無法啟動。",
    "auto.components.settings.recoverServer.checking": "正在檢查鎖定…",
    "auto.components.settings.recoverServer.confirmCheck": "確認共用此使用者目錄的其他機器均未執行 Orca",
    "auto.components.settings.recoverServer.cancel": "取消",
    "auto.components.settings.recoverServer.confirm": "清除鎖定並重新啟動",
    "auto.components.settings.recoverServer.eligible": "在此機器的舊位址上沒有任何回應，但 Orca 無法排除有同名機器共用此家目錄的可能。",
    "auto.components.settings.recoverServer.host": "主機",
    "auto.components.settings.recoverServer.lockBoot": "開機期間寫入",
    "auto.components.settings.recoverServer.currentBoot": "目前開機階段",
    "auto.components.settings.recoverServer.warning": "僅在確認共用此家目錄的其他機器均未為此設定檔執行 Orca 時，方可繼續。",
    "auto.components.settings.recoverServer.none": "已無需要清除的鎖定檔。請重新連線以啟動此主機的 Orca 伺服器。",
    "auto.components.settings.recoverServer.manualCommand": "在主機上執行此指令，或刪除「詳細資訊」中顯示的鎖定檔：",
    "auto.components.settings.recoverServer.manualDelete": "一旦確定沒有其他機器使用該鎖定檔，即可刪除「詳細資訊」中顯示的鎖定檔。",
    "auto.components.settings.recoverServer.action": "復原伺服器…",
    "auto.components.settings.recoverServer.written": "已寫入",
    "auto.components.settings.recoverServer.manualDeleteCommand": "手動刪除主機上的鎖定檔：",
    "auto.components.settings.recoverServer.manualDeleteWarning": "僅在確認共用此家目錄的其他機器均未為此設定檔執行 Orca 時方可執行此操作。",
    "auto.components.settings.recoverServer.close": "關閉",
    "auto.components.settings.recoverServer.reclaimedNotStarted": "鎖定已清除，但 Orca 伺服器未能啟動。",
    "auto.components.settings.claudeSubagentNavigation.title": "Claude 子 Agent（Subagent）導覽",
    "auto.components.settings.claudeSubagentNavigation.description": "從側邊欄開啟 Claude 子 Agent。將快速鍵新增至 Claude 的 keybindings.json，並在新的 Orca 窗格中載入 Orca mod。需使用 Claude 2.1.300+ 及狀態勾點（Status Hook）。關閉此功能將移除 Orca 的快速鍵；您手動刪除的快速鍵將保持刪除狀態。",
    "auto.components.settings.claudeSubagentNavigation.search.subagent": "子 Agent",
    "auto.components.settings.claudeSubagentNavigation.search.navigation": "導覽",
    "auto.components.settings.claudeSubagentNavigation.search.plugin": "外掛",
    "auto.components.settings.claudeSubagentNavigation.search.mod": "mod",
    "auto.components.settings.claudeSubagentNavigation.search.shortcut": "快速鍵",
    "auto.components.right.sidebar.source.control.dropdown.items.checkingBranchStatus": "正在檢查分支狀態…",
    "auto.components.right.sidebar.source.control.dropdown.items.titleCheckingPrStatus": "正在檢查 PR 狀態…",
    "auto.components.right.sidebar.source.control.dropdown.items.titlePrAlreadyMerged": "PR 已經合併",
    "auto.components.right.sidebar.source.control.dropdown.items.titleCheckOutBranchToSync": "簽出分支後再同步提交",
    "auto.components.right.sidebar.source.control.dropdown.items.titlePublishBranchFirst": "請先發佈分支以同步提交",
    "auto.components.right.sidebar.source.control.dropdown.items.titleUseForcePush": "使用「提交並強制推送（Force Push）」— 遠端僅包含本機提交的舊複本",
    "auto.components.right.sidebar.source.control.dropdown.items.titleCommitThenPullPush": "先提交，再提取（Pull）並推送（Push）",
    "auto.components.right.sidebar.source.control.dropdown.items.rebaseFromNamedBase": "從 {{baseRef}} 變基（Rebase）",
    "auto.components.right.sidebar.source.control.dropdown.items.rebaseFromBase": "從基礎分支變基（Rebase）",
    "auto.components.right.sidebar.source.control.dropdown.items.rebaseChooseRemoteBase": "選擇要從中進行變基的遠端基礎分支",
    "auto.components.right.sidebar.source.control.dropdown.items.rebaseDirtyHint": "嘗試進行變基；Git 可能要求先提交或暫存（Stash）本機變更",
    "auto.components.right.sidebar.source.control.dropdown.items.rebaseWithLatestFrom": "使用 {{baseRef}} 的最新提交對目前分支進行變基",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedCommitFirst": "請先提交變更",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedCheckOutBranchFirst": "請先簽出分支",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedSwitchToFeatureBranch": "切換至功能分支",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedPublishBranch": "發佈分支",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedPushFirst": "請先推送",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedForcePushFirst": "請先強制推送（Force Push）",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedSyncFirst": "請先同步",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedAuthRequired": "在此環境中{{authInstruction}}",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedUnsupportedProvider": "不支援的提供者",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedExistingReview": "{{reviewLabel}} 已存在",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedForkHeadUnsupported": "不支援 Fork Head",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedBaseNotOnRemote": "基礎分支不存在於遠端",
    "auto.components.right.sidebar.source.control.dropdown.items.blockedBranchNotReady": "分支尚未就緒",
    "auto.components.ClaudeAgentViewIndicator.viewing": "目前檢視中",
    "auto.components.ClaudeAgentViewIndicator.viewingChild": "正在檢視子 Agent {{name}}",
    "auto.components.ClaudeAgentViewIndicator.returnHint": "點選父層列以返回。按 Esc 停止此子 Agent。按 Enter 將草稿傳送給此子 Agent。",
    "components.native-chat.writeNotice.notDoneGoalChangeIncomplete": "未能完成目標變更。請查看聊天視窗。",
    "components.terminalPane.hostFile.updateHostForOutsideFiles": "更新 {{value0}} 上的 Orca 以開啟其工作區以外的檔案",
    "accounts.claude.switchSessions.uncheckedOne": "無法為 Claude 檢查 1 個終端機。若 Claude 正在該處執行，它將保持在 {{previous}} 直到重新啟動。",
    "accounts.claude.switchSessions.uncheckedOther": "無法為 Claude 檢查 {{count}} 個終端機。任何在該處執行的 Claude 都將保持在 {{previous}} 直到重新啟動。",
    "nativeChat.math.scrollDisplayEquation": "捲動顯示方程式",
}

cc = opencc.OpenCC('s2twp')

def convert_zh_to_zh_tw(s: str) -> str:
    t = cc.convert(s)
    # Domain specific terminology replacements for Taiwan
    t = t.replace('選項卡', '分頁')
    t = t.replace('標籤頁', '分頁')
    t = t.replace('刷新', '重新整理')
    t = t.replace('會話', '工作階段')
    t = t.replace('撤銷', '復原')
    t = t.replace('客戶端', '使用者端')
    t = t.replace('快捷鍵', '快速鍵')
    t = t.replace('源代碼', '原始碼')
    t = t.replace('源碼', '原始碼')
    t = t.replace('代碼', '程式碼')
    t = re.sub(r'終端(?!機)', '終端機', t)
    t = t.replace('倉庫', '儲存庫')
    t = t.replace('檔案夾', '資料夾')
    t = t.replace('文件夾', '資料夾')
    t = t.replace('保存', '儲存')
    t = t.replace('創建', '建立')
    t = t.replace('網絡', '網路')
    t = t.replace('圖標', '圖示')
    t = t.replace('屏幕', '螢幕')
    t = t.replace('高清', '高畫質')
    t = t.replace('進程', '處理程序')
    t = t.replace('線程', '執行緒')
    t = t.replace('回車', 'Enter')
    t = t.replace('日誌', '記錄')
    return t

def flatten_dict(d, prefix=''):
    res = {}
    for k, v in d.items():
        cur = f'{prefix}.{k}' if prefix else k
        if isinstance(v, dict):
            res.update(flatten_dict(v, cur))
        elif isinstance(v, str):
            res[cur] = v
    return res

def unflatten_dict(flat):
    root = {}
    for k, v in flat.items():
        parts = k.split('.')
        cur = root
        for p in parts[:-1]:
            if p not in cur:
                cur[p] = {}
            cur = cur[p]
        cur[parts[-1]] = v
    return root

def main():
    print("Loading locale files...")
    with open(UPSTREAM_EN, 'r', encoding='utf-8') as f:
        en = json.load(f)
    with open(UPSTREAM_ZH, 'r', encoding='utf-8') as f:
        zh = json.load(f)
    with open(CURRENT_ZH_TW, 'r', encoding='utf-8') as f:
        zh_tw_cur = json.load(f)

    en_flat = flatten_dict(en)
    zh_flat = flatten_dict(zh)
    tw_flat = flatten_dict(zh_tw_cur)

    # Patch known existing errors
    tw_flat['auto.components.sidebar.SidebarFeedbackImageAttachments.screenshotsHint'] = \
        '最多可附加 {{count}} 張螢幕截圖，合計不超過 {{maxSize}}'

    print(f"Upstream en leaf keys: {len(en_flat)}")
    print(f"Upstream zh leaf keys: {len(zh_flat)}")
    print(f"Current zh-TW leaf keys: {len(tw_flat)}")

    ph_re = re.compile(r'\{\{[^}]+\}\}')

    result_flat = {}
    reused_tw = 0
    from_manual = 0
    converted_zh = 0
    fallback_en = 0
    excluded_protected = 0

    for key, en_val in en_flat.items():
        if is_protected_path(key):
            excluded_protected += 1
            continue

        if len(en_val) > 8192:
            print(f"Skipping key with value > 8192 chars: {key}")
            continue

        en_phs = sorted(ph_re.findall(en_val))

        # 1. Manual translation takes precedence if specified for newly missing keys
        if key in MANUAL_TRANSLATIONS:
            val = MANUAL_TRANSLATIONS[key]
            from_manual += 1
        # 2. Re-use existing zh-TW translation if available
        elif key in tw_flat:
            val = tw_flat[key]
            reused_tw += 1
        # 3. Convert from upstream zh.json
        elif key in zh_flat:
            val = convert_zh_to_zh_tw(zh_flat[key])
            converted_zh += 1
        # 4. Fallback to English
        else:
            val = en_val
            fallback_en += 1

        # Check placeholder integrity
        val_phs = sorted(ph_re.findall(val))
        if en_phs != val_phs:
            print(f"WARNING: placeholder mismatch at {key}!")
            print(f"  EN:  {en_val} -> {en_phs}")
            print(f"  VAL: {val} -> {val_phs}")
            # If placeholders mismatched, fallback to English with note
            val = en_val

        result_flat[key] = val

    print(f"\nTranslation stats:")
    print(f"  Reused from zh-TW: {reused_tw}")
    print(f"  From manual translations: {from_manual}")
    print(f"  Converted from zh.json: {converted_zh}")
    print(f"  Fallback to en: {fallback_en}")
    print(f"  Excluded protected: {excluded_protected}")
    print(f"  Total translated keys: {len(result_flat)}")

    # Build nested catalog in exact key order matching en.json
    def build_tree(en_node, path=''):
        res = {}
        for k, v in en_node.items():
            cur = f'{path}.{k}' if path else k
            if isinstance(v, dict):
                if is_protected_path(cur) and not is_container_path(cur):
                    continue
                child = build_tree(v, cur)
                if child:
                    res[k] = child
            elif isinstance(v, str):
                if cur in result_flat:
                    res[k] = result_flat[cur]
        return res

    new_tree = build_tree(en)

    # Validate catalog against parsePluginLanguagePackArtifact rules
    PLUGIN_LANGUAGE_CATALOG_MAX_ENTRIES = 20_000
    PLUGIN_LANGUAGE_CATALOG_MAX_DEPTH = 16
    DANGEROUS_KEYS = {'__proto__', 'prototype', 'constructor'}

    stack = [(new_tree, '', 0)]
    entry_count = 0
    validation_passed = True

    while stack:
        frame_source, frame_path, frame_depth = stack.pop()
        if frame_depth > PLUGIN_LANGUAGE_CATALOG_MAX_DEPTH:
            print(f"ERROR: depth {frame_depth} exceeded at {frame_path}")
            validation_passed = False
            break
        for k, val in frame_source.items():
            entry_count += 1
            if entry_count > PLUGIN_LANGUAGE_CATALOG_MAX_ENTRIES:
                print(f"ERROR: entry count exceeded {PLUGIN_LANGUAGE_CATALOG_MAX_ENTRIES}")
                validation_passed = False
                break
            if len(k) == 0 or len(k) > 128 or k in DANGEROUS_KEYS or '.' in k:
                print(f"ERROR: unsafe key: {k} at {frame_path}")
                validation_passed = False
                break
            full_path = f'{frame_path}.{k}' if frame_path else k
            is_obj = isinstance(val, dict)
            if is_protected_path(full_path) and not (is_obj and is_container_path(full_path)):
                print(f"ERROR: protected translation at {full_path}")
                validation_passed = False
                break
            if isinstance(val, str):
                if len(val) > 8192:
                    print(f"ERROR: value exceeds 8192 chars at {full_path}")
                    validation_passed = False
                    break
            elif is_obj:
                stack.append((val, full_path, frame_depth + 1))
            else:
                print(f"ERROR: value must be string or dict at {full_path}")
                validation_passed = False
                break

    print(f"\nCatalog validation result: {'PASSED' if validation_passed else 'FAILED'}")
    print(f"Total entries (nodes + leaves): {entry_count} (Limit: {PLUGIN_LANGUAGE_CATALOG_MAX_ENTRIES})")

    if not validation_passed:
        print("Aborting write due to validation failure.")
        sys.exit(1)

    print(f"Writing to {OUTPUT_ZH_TW}...")
    with open(OUTPUT_ZH_TW, 'w', encoding='utf-8') as f:
        json.dump(new_tree, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print("Success! Updated zh-TW.json has been written.")

if __name__ == '__main__':
    main()
