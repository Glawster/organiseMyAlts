local oma = organiseMyAlts

-- Layout constants
local FRAME_WIDTH         = 740
local FRAME_HEIGHT        = 400
local CONTENT_LEFT        = 14
local CONTENT_TOP_Y       = -30
local COL_HDR_Y           = -54
local ROW_START_Y         = -74
local ROW_HEIGHT          = 17
local MAX_CHAR_ROWS       = 16

-- Column x-offsets from the left edge of the frame content area
local COL = {
    char    = CONTENT_LEFT,
    class   = CONTENT_LEFT + 190,
    spec    = CONTENT_LEFT + 280,
    level   = CONTENT_LEFT + 390,
    ilvl    = CONTENT_LEFT + 435,
    scanned = CONTENT_LEFT + 490,
    lastscan = CONTENT_LEFT + 560,
}

local function formatTimestamp(ts)
    local dateFn = nil
    if os and type(os.date) == "function" then
        dateFn = os.date
    elseif type(date) == "function" then
        dateFn = date
    end
    if not ts then
        return "---"
    end
    if not dateFn then
        return tostring(ts)
    end
    return dateFn("%m-%d %H:%M", ts)
end

-- Returns the latest keybind snapshot timestamp for a character (any spec).
function oma:getLatestKeybindScanTs(characterKey)
    local snapshots = self.db and self.db.keybinds and self.db.keybinds.snapshots or {}
    local latestTs = nil
    for _, snapshot in ipairs(snapshots) do
        if snapshot.character == characterKey then
            if snapshot.ts and (not latestTs or snapshot.ts > latestTs) then
                latestTs = snapshot.ts
            end
        end
    end
    return latestTs
end

function oma:getKeybindSnapshotScanStatus(characterKey, specID, talentLoadoutID)
    local snapshots = self.db and self.db.keybinds and self.db.keybinds.snapshots or {}
    local count = 0
    local latestTs = nil

    for _, snapshot in ipairs(snapshots) do
        if snapshot.character == characterKey and snapshot.specID == specID and snapshot.talentLoadoutID == talentLoadoutID then
            count = count + 1
            if snapshot.ts and (not latestTs or snapshot.ts > latestTs) then
                latestTs = snapshot.ts
            end
        end
    end

    return count > 0, count, latestTs
end

-- Builds the sorted list of all tracked characters for display.
-- Returns rows sorted by lastScan descending, then lastLogin descending.
function oma:getCharacterStatusRows()
    local characters = self.db and self.db.characters or {}
    local rows = {}

    for key, char in pairs(characters) do
        local latestScanTs = self:getLatestKeybindScanTs(key)
        table.insert(rows, {
            characterKey  = key,
            name          = char.name or key,
            class         = char.class or "?",
            specName      = char.specName or "?",
            level         = char.level or 0,
            ilvl          = char.equippedItemLevel or char.averageItemLevel or 0,
            lastScan      = char.lastScan or 0,
            lastLogin     = char.lastLogin or 0,
            keybindTs     = latestScanTs,
        })
    end

    table.sort(rows, function(a, b)
        local aTs = math.max(a.lastScan or 0, a.lastLogin or 0)
        local bTs = math.max(b.lastScan or 0, b.lastLogin or 0)
        return aTs > bTs
    end)

    return rows
end

-- Creates a single row of column FontStrings anchored to the frame.
local function createRowCells(frame, yOffset, fontTemplate)
    local cells = {}
    local colKeys = { "char", "class", "spec", "level", "ilvl", "scanned", "lastscan" }
    for _, colKey in ipairs(colKeys) do
        local fs = frame:CreateFontString(nil, "OVERLAY", fontTemplate or "GameFontNormalSmall")
        fs:SetPoint("TOPLEFT", frame, "TOPLEFT", COL[colKey], yOffset)
        fs:SetJustifyH("LEFT")
        fs:SetText("")
        cells[colKey] = fs
    end
    return cells
end

-- Colours a row of cells based on whether it is the current character.
local function tintRowCells(cells, isCurrent)
    local r, g, b = isCurrent and 1 or 0.9, isCurrent and 1 or 0.9, isCurrent and 0 or 0.9
    for _, fs in pairs(cells) do
        fs:SetTextColor(r, g, b)
    end
end

function oma:ensureKeybindStatusFrame()
    if self.keybindStatusFrame then
        return self.keybindStatusFrame
    end

    local frame = CreateFrame("Frame", "organiseMyAltsKeybindStatusFrame", UIParent, "BasicFrameTemplateWithInset")
    frame:SetSize(FRAME_WIDTH, FRAME_HEIGHT)
    frame:SetPoint("CENTER")
    frame:SetMovable(true)
    frame:EnableMouse(true)
    frame:RegisterForDrag("LeftButton")
    frame:SetScript("OnDragStart", frame.StartMoving)
    frame:SetScript("OnDragStop", frame.StopMovingOrSizing)
    frame:Hide()

    -- Title
    frame.title = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
    frame.title:SetPoint("TOP", frame, "TOP", 0, -8)
    frame.title:SetText("organiseMyAlts — Character Overview")

    -- Current character summary line
    frame.currentLine = frame:CreateFontString(nil, "OVERLAY", "GameFontNormal")
    frame.currentLine:SetPoint("TOPLEFT", frame, "TOPLEFT", CONTENT_LEFT, CONTENT_TOP_Y)
    frame.currentLine:SetJustifyH("LEFT")
    frame.currentLine:SetText("")

    -- Divider texture
    frame.divider = frame:CreateTexture(nil, "ARTWORK")
    frame.divider:SetColorTexture(0.4, 0.4, 0.4, 0.6)
    frame.divider:SetSize(FRAME_WIDTH - 30, 1)
    frame.divider:SetPoint("TOPLEFT", frame, "TOPLEFT", CONTENT_LEFT, COL_HDR_Y - 2)

    -- Column header cells
    frame.colHeaders = createRowCells(frame, COL_HDR_Y, "GameFontHighlightSmall")
    frame.colHeaders.char:SetText("Character")
    frame.colHeaders.class:SetText("Class")
    frame.colHeaders.spec:SetText("Spec")
    frame.colHeaders.level:SetText("Lvl")
    frame.colHeaders.ilvl:SetText("iLvl")
    frame.colHeaders.scanned:SetText("KB Scan")
    frame.colHeaders.lastscan:SetText("Last Scan")

    -- Data rows
    frame.charRows = {}
    for i = 1, MAX_CHAR_ROWS do
        local yOff = ROW_START_Y - (i - 1) * ROW_HEIGHT
        frame.charRows[i] = createRowCells(frame, yOff, "GameFontNormalSmall")
    end

    -- Empty state label
    frame.emptyLabel = frame:CreateFontString(nil, "OVERLAY", "GameFontNormalSmall")
    frame.emptyLabel:SetPoint("TOPLEFT", frame, "TOPLEFT", CONTENT_LEFT, ROW_START_Y)
    frame.emptyLabel:SetText("No characters tracked yet. Log in to each character and run /oma scan.")
    frame.emptyLabel:Hide()

    self.keybindStatusFrame = frame
    return frame
end

function oma:refreshKeybindStatusUI()
    local frame = self:ensureKeybindStatusFrame()
    local currentKey  = self:getCurrentCharacterKey() or ""
    local specID, specName = self:getCurrentSpecInfo()
    local talentLoadoutID  = self:getCurrentTalentLoadoutID()
    local scanned, scansForCombo = self:getKeybindSnapshotScanStatus(currentKey, specID, talentLoadoutID)

    -- Current character summary line
    frame.currentLine:SetText(
        string.format(
            "Current: %s  |  %s  |  talents %s  |  keybind scanned: %s (%d)",
            currentKey ~= "" and currentKey or "unknown",
            specName or "?",
            tostring(talentLoadoutID or "none"),
            scanned and "|cff00ff00YES|r" or "|cffff4444NO|r",
            scansForCombo or 0
        )
    )

    -- Populate data rows
    local rows = self:getCharacterStatusRows()
    local hasData = #rows > 0

    frame.emptyLabel:SetShown(not hasData)

    for i = 1, MAX_CHAR_ROWS do
        local cells = frame.charRows[i]
        local row = rows[i]

        if row then
            local isCurrent = row.characterKey == currentKey
            local kbTs = row.keybindTs
            local kbText = kbTs and ("|cff00ff00YES|r") or "|cffff4444NO|r"
            local lastScanText = row.lastScan and row.lastScan > 0 and formatTimestamp(row.lastScan) or "---"

            cells.char:SetText(row.name or row.characterKey)
            cells.class:SetText(row.class)
            cells.spec:SetText(row.specName)
            cells.level:SetText(tostring(row.level))
            cells.ilvl:SetText(row.ilvl > 0 and string.format("%d", row.ilvl) or "?")
            cells.scanned:SetText(kbText)
            cells.lastscan:SetText(lastScanText)

            tintRowCells(cells, isCurrent)
        else
            for _, fs in pairs(cells) do
                fs:SetText("")
            end
        end
    end

    self:logDebug(
        string.format(
            "event=keybind.ui.refresh char=%s spec=%s scanned=%s scans=%d total_chars=%d",
            currentKey,
            tostring(specName or "?"),
            scanned and "true" or "false",
            scansForCombo or 0,
            #rows
        )
    )

    return scanned, scansForCombo
end

function oma:toggleKeybindStatusUI()
    local frame = self:ensureKeybindStatusFrame()
    self.db.uiState = self.db.uiState or {}

    if frame:IsShown() then
        frame:Hide()
        self.db.uiState.keybindStatusVisible = false
        self:print("ui: character overview hidden")
        self:log("INFO", "event=keybind.ui.toggle visible=false source=slash_ui")
        return
    end

    self:refreshKeybindStatusUI()
    frame:Show()
    self.db.uiState.keybindStatusVisible = true
    self:print("ui: character overview shown")
    self:log("INFO", "event=keybind.ui.toggle visible=true source=slash_ui")
end
