local oma = organiseMyAlts

local MAX_STATUS_ROWS = 10

local function formatTimestamp(ts)
    local dateFn = date or (os and os.date)
    if not ts then
        return "unknown"
    end
    if not dateFn then
        return tostring(ts)
    end
    return dateFn("%Y-%m-%d %H:%M", ts)
end

function oma:getKeybindSnapshotScanStatus(characterKey, specID, talentLoadoutID)
    local snapshots = self.db and self.db.keybinds and self.db.keybinds.snapshots or {}
    local count = 0
    local latestTs = nil

    for _, snapshot in ipairs(snapshots) do
        if snapshot.character == characterKey and snapshot.specID == specID and snapshot.talentLoadoutID == talentLoadoutID then
            count = count + 1
            if not latestTs or (snapshot.ts and snapshot.ts > latestTs) then
                latestTs = snapshot.ts
            end
        end
    end

    return count > 0, count, latestTs
end

function oma:getKeybindSnapshotStatusRows(limit)
    local snapshots = self.db and self.db.keybinds and self.db.keybinds.snapshots or {}
    local combos = {}
    local ordered = {}

    for _, snapshot in ipairs(snapshots) do
        local comboKey = table.concat({
            snapshot.character or "unknown-character",
            tostring(snapshot.specID or 0),
            tostring(snapshot.talentLoadoutID or 0),
        }, "::")

        local row = combos[comboKey]
        if not row then
            row = {
                character = snapshot.character or "unknown-character",
                specName = snapshot.specName or "unknown-spec",
                talentLoadoutID = snapshot.talentLoadoutID,
                count = 0,
                latestTs = snapshot.ts or 0,
            }
            combos[comboKey] = row
            table.insert(ordered, row)
        end

        row.count = row.count + 1
        if (snapshot.ts or 0) > row.latestTs then
            row.latestTs = snapshot.ts or 0
        end
    end

    table.sort(ordered, function(a, b)
        return (a.latestTs or 0) > (b.latestTs or 0)
    end)

    local maxRows = math.min(limit or MAX_STATUS_ROWS, #ordered)
    local rows = {}
    for i = 1, maxRows do
        rows[i] = ordered[i]
    end
    return rows
end

function oma:ensureKeybindStatusFrame()
    if self.keybindStatusFrame then
        return self.keybindStatusFrame
    end

    local frame = CreateFrame("Frame", "organiseMyAltsKeybindStatusFrame", UIParent, "BasicFrameTemplateWithInset")
    frame:SetSize(620, 300)
    frame:SetPoint("CENTER")
    frame:SetMovable(true)
    frame:EnableMouse(true)
    frame:RegisterForDrag("LeftButton")
    frame:SetScript("OnDragStart", frame.StartMoving)
    frame:SetScript("OnDragStop", frame.StopMovingOrSizing)
    frame:Hide()

    frame.title = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    frame.title:SetPoint("TOP", frame, "TOP", 0, -8)
    frame.title:SetText("organiseMyAlts - Keybind Scan Status")

    frame.current = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    frame.current:SetPoint("TOPLEFT", frame, "TOPLEFT", 16, -34)
    frame.current:SetJustifyH("LEFT")
    frame.current:SetText("")

    frame.header = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlightSmall")
    frame.header:SetPoint("TOPLEFT", frame.current, "BOTTOMLEFT", 0, -12)
    frame.header:SetJustifyH("LEFT")
    frame.header:SetText("Recent scanned combinations:")

    frame.rows = {}
    for i = 1, MAX_STATUS_ROWS do
        local row = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
        row:SetPoint("TOPLEFT", frame.header, "BOTTOMLEFT", 0, -((i - 1) * 16) - 6)
        row:SetJustifyH("LEFT")
        row:SetText("")
        frame.rows[i] = row
    end

    self.keybindStatusFrame = frame
    return frame
end

function oma:refreshKeybindStatusUI()
    local frame = self:ensureKeybindStatusFrame()
    local characterKey = self:getCurrentCharacterKey() or "unknown-character"
    local specID, specName = self:getCurrentSpecInfo()
    local talentLoadoutID = self:getCurrentTalentLoadoutID()
    local scanned, scansForCombo, latestTs = self:getKeybindSnapshotScanStatus(characterKey, specID, talentLoadoutID)

    frame.current:SetText(
        string.format(
            "Current: %s | %s | talents %s | scanned %s (%d)",
            characterKey,
            specName or "unknown-spec",
            tostring(talentLoadoutID or "none"),
            scanned and "YES" or "NO",
            scansForCombo or 0
        )
    )

    local rows = self:getKeybindSnapshotStatusRows(MAX_STATUS_ROWS)
    for i = 1, MAX_STATUS_ROWS do
        local row = rows[i]
        if row then
            frame.rows[i]:SetText(
                string.format(
                    "%s | %s | talents %s | scans %d | last %s",
                    row.character or "unknown-character",
                    row.specName or "unknown-spec",
                    tostring(row.talentLoadoutID or "none"),
                    row.count or 0,
                    formatTimestamp(row.latestTs)
                )
            )
        elseif i == 1 then
            frame.rows[i]:SetText("No scanned combinations yet. Use /oma scan or /oma keybinds.")
        else
            frame.rows[i]:SetText("")
        end
    end

    self:logDebug(
        string.format(
            "event=keybind.ui.refresh char=%s spec=%s scanned=%s scans=%d",
            characterKey,
            tostring(specName or "unknown-spec"),
            scanned and "true" or "false",
            scansForCombo or 0
        )
    )

    return scanned, scansForCombo, latestTs
end

function oma:toggleKeybindStatusUI()
    local frame = self:ensureKeybindStatusFrame()
    self.db.uiState = self.db.uiState or {}

    if frame:IsShown() then
        frame:Hide()
        self.db.uiState.keybindStatusVisible = false
        self:print("ui: keybind scan status hidden")
        self:log("INFO", "event=keybind.ui.toggle visible=false source=slash_ui")
        return
    end

    self:refreshKeybindStatusUI()
    frame:Show()
    self.db.uiState.keybindStatusVisible = true
    self:print("ui: keybind scan status shown")
    self:log("INFO", "event=keybind.ui.toggle visible=true source=slash_ui")
end
