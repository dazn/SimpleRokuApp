sub init()
    m.fileList   = m.top.findNode("fileList")
    m.statusLabel = m.top.findNode("statusLabel")
    m.video      = m.top.findNode("Video")
    m.fetcher    = m.top.findNode("fetcher")
    m.warning    = m.top.findNode("WarningDialog")
    m.exiter     = m.top.findNode("Exiter")

    m.currentPath = ""
    m.entries     = []

    m.fetcher.observeField("status", "onFetchStatus")
    m.fileList.observeField("itemSelected", "onItemSelected")
    m.video.observeField("state", "onVideoState")
    m.warning.observeField("buttonSelected", "onWarningClosed")

    m.statusLabel.text    = "Loading..."
    m.statusLabel.visible = true
    m.fileList.visible    = false

    m.fetcher.path    = ""
    m.fetcher.control = "RUN"
end sub

sub onFetchStatus()
    if m.fetcher.status = "done"
        m.entries = m.fetcher.entries
        if m.entries = invalid
            m.entries = []
        end if
        populateList()
        m.statusLabel.visible = false
        m.fileList.visible    = true
        m.fileList.setFocus(true)
    else if m.fetcher.status = "error"
        m.statusLabel.text    = "Error loading directory"
        m.statusLabel.visible = true
    end if
end sub

sub populateList()
    root = CreateObject("roSGNode", "ContentNode")
    for each entry in m.entries
        node                = root.CreateChild("ContentNode")
        node.TITLE          = entry.name
        node.HDGRIDPOSTERURL = entry.iconUri
    end for
    m.fileList.content = root
end sub

sub onItemSelected()
    index = m.fileList.itemSelected
    if index < 0 or index >= m.entries.Count()
        return
    end if
    entry = m.entries[index]
    if entry.type = "directory"
        goToPath(entry.path)
    else
        playVideo(entry)
    end if
end sub

function toRokuStreamFormat(sf as String) as String
    if sf = "" then return ""   ' no format info — caller should show error
    if sf = "mp4"  then return "mp4"
    if sf = "mp3"  then return "mp3"
    if sf = "hls"  then return "hls"
    if sf = "dash" then return "dash"
    if sf = "mkv"  then return "mkv"
    if sf = "mka"  then return "mkv"
    if sf = "mks"  then return "mkv"
    return sf   ' pass unknown formats through and let the player try
end function

sub playVideo(entry as Object)
    fmt = toRokuStreamFormat(entry.streamFormat)
    if fmt = ""
        m.warning.message = "'" + entry.name + "' cannot be played (no format information)."
        m.warning.visible = true
        m.warning.setFocus(true)
        return
    end if
    contentNode = CreateObject("roSGNode", "ContentNode")
    contentNode.url          = entry.url
    contentNode.streamFormat = fmt
    contentNode.HttpHeaders  = ["Authorization: Bearer " + getApiKey()]
    m.video.content          = contentNode
    m.video.visible     = true
    m.video.control     = "play"
    m.video.setFocus(true)
end sub

sub onWarningClosed()
    m.warning.visible = false
    m.fileList.setFocus(true)
end sub

sub onVideoState()
    state = m.video.state
    if state = "error" or state = "finished"
        m.video.control    = "stop"
        m.video.visible    = false
        m.fileList.visible = true
        m.fileList.setFocus(true)
    end if
end sub

sub goToPath(path as String)
    m.currentPath         = path
    m.statusLabel.text    = "Loading..."
    m.statusLabel.visible = true
    m.fileList.visible    = false
    m.fetcher.control     = "STOP"
    m.fetcher.status      = ""
    m.fetcher.path        = path
    m.fetcher.control     = "RUN"
end sub

function getParentPath(path as String) as String
    if path = "" then return ""
    parts = path.Split("/")
    if parts.Count() <= 1 then return ""
    result = parts[0]
    for i = 1 to parts.Count() - 2
        result = result + "/" + parts[i]
    end for
    return result
end function

function onKeyEvent(key as String, press as Boolean) as Boolean
    if press
        if key = "back"
            if m.video.visible
                m.video.control   = "stop"
                m.video.visible   = false
                m.fileList.visible = true
                m.fileList.setFocus(true)
                return true
            else if m.currentPath <> ""
                goToPath(getParentPath(m.currentPath))
                return true
            else
                return false
            end if
        end if
    end if
    return false
end function
