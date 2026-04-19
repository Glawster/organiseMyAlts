local oma = organiseMyAlts

-- Layout constants
local FRAME_WIDTH         = 860
local FRAME_HEIGHT        = 400
local CONTENT_LEFT        = 14
local COL_HDR_Y           = -36
local ROW_START_Y         = -56
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
    lastscan = CONTENT_LEFT + 636,
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

-- Returns "Name" from "NAME" (sentence case).
local function toSentenceCase(s)
    if not s or s == "" then return s end
    return s:sub(1, 1):upper() .. s:sub(2):lower()
end

-- Returns r, g, b for a WoW class name using RAID_CLASS_COLORS when available.
local CLASS_COLORS_FALLBACK = {
    DEATHKNIGHT = {0.77, 0.12, 0.23},
    DEMONHUNTER = {0.64, 0.19, 0.79},
    DRUID       = {1.00, 0.49, 0.04},
    EVOKER      = {0.20, 0.58, 0.50},
    HUNTER      = {0.67, 0.83, 0.45},
    MAGE        = {0.25, 0.78, 0.92},
    MONK        = {0.00, 1.00, 0.60},
    PALADIN     = {0.96, 0.55, 0.73},
    PRIEST      = {1.00, 1.00, 1.00},
    ROGUE       = {1.00, 0.96, 0.41},
    SHAMAN      = {0.00, 0.44, 0.87},
    WARLOCK     = {0.53, 0.53, 0.93},
    WARRIOR     = {0.78, 0.61, 0.23},
}

local function getClassColor(className)
    if RAID_CLASS_COLORS and RAID_CLASS_COLORS[className] then
        local c = RAID_CLASS_COLORS[className]
        return c.r, c.g, c.b
    end
    local c = CLASS_COLORS_FALLBACK[className]
    if c then return c[1], c[2], c[3] end
    return 0.9, 0.9, 0.9
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

-- Returns the first 4 characters of a spec name for compact display.
local function specAbbrev(name)
    if not name or name == "" then return "?" end
    return name:sub(1, 4)
end

-- Returns a sorted list of unique spec names that have at least one snapshot
-- for the given character key.
function oma:getScannedSpecNamesForCharacter(characterKey)
    local snapshots = self.db and self.db.keybinds and self.db.keybinds.snapshots or {}
    local seen = {}
    local list = {}
    for _, snapshot in ipairs(snapshots) do
        if snapshot.character == characterKey and snapshot.specName and not seen[snapshot.specName] then
            seen[snapshot.specName] = true
            table.insert(list, snapshot.specName)
        end
    end
    table.sort(list)
    return list
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
            characterKey     = key,
            name             = char.name or key,
            class            = char.class or "?",
            specName         = char.specName or "?",
            level            = char.level or 0,
            ilvl             = char.equippedItemLevel or char.averageItemLevel or 0,
            lastScan         = char.lastScan or 0,
            lastLogin        = char.lastLogin or 0,
            keybindTs        = latestScanTs,
            scannedSpecNames = self:getScannedSpecNamesForCharacter(key),
        })
    end

    -- Sort by lastScan descending so the displayed "Last Scan" column matches the order.
    -- Fall back to lastLogin for characters that have never been scanned.
    table.sort(rows, function(a, b)
        local aTs = (a.lastScan and a.lastScan > 0) and a.lastScan or (a.lastLogin or 0)
        local bTs = (b.lastScan and b.lastScan > 0) and b.lastScan or (b.lastLogin or 0)
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

-- Colours a row of cells. Non-class cells use yellow (current) or white (other).
-- The class cell always uses the WoW class colour.
local function tintRowCells(cells, isCurrent, className)
    local r, g, b = isCurrent and 1 or 0.9, isCurrent and 1 or 0.9, isCurrent and 0 or 0.9
    for key, fs in pairs(cells) do
        if key == "class" then
            fs:SetTextColor(getClassColor(className))
        else
            fs:SetTextColor(r, g, b)
        end
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
    frame.colHeaders.scanned:SetText("KB Specs")
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

    -- Register with the game engine so Escape closes the frame automatically.
    table.insert(UISpecialFrames, "organiseMyAltsKeybindStatusFrame")

    self.keybindStatusFrame = frame
    return frame
end

function oma:refreshKeybindStatusUI()
    local frame = self:ensureKeybindStatusFrame()
    local currentKey  = self:getCurrentCharacterKey() or ""
    local specID, specName = self:getCurrentSpecInfo()
    local talentLoadoutID  = self:getCurrentTalentLoadoutID()
    local scanned, scansForCombo = self:getKeybindSnapshotScanStatus(currentKey, specID, talentLoadoutID)

    -- Populate data rows
    local rows = self:getCharacterStatusRows()
    local hasData = #rows > 0

    frame.emptyLabel:SetShown(not hasData)

    for i = 1, MAX_CHAR_ROWS do
        local cells = frame.charRows[i]
        local row = rows[i]

        if row then
            local isCurrent = row.characterKey == currentKey
            local specNames = row.scannedSpecNames or {}
            local kbText
            if #specNames == 0 then
                kbText = "|cffff4444------|r"
            else
                local parts = {}
                for _, name in ipairs(specNames) do
                    table.insert(parts, specAbbrev(name))
                end
                kbText = "|cff00ff00" .. table.concat(parts, "/") .. "|r"
            end
            local lastScanText = row.lastScan and row.lastScan > 0 and formatTimestamp(row.lastScan) or "---"

            cells.char:SetText(row.name or row.characterKey)
            cells.class:SetText(toSentenceCase(row.class))
            cells.spec:SetText(row.specName)
            cells.level:SetText(tostring(row.level))
            cells.ilvl:SetText((row.ilvl and row.ilvl > 0) and string.format("%d", row.ilvl) or "?")
            cells.scanned:SetText(kbText)
            cells.lastscan:SetText(lastScanText)

            tintRowCells(cells, isCurrent, row.class)
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
