sub init()
    m.focusBg = m.top.findNode("focusBg")
    m.icon    = m.top.findNode("icon")
    m.label   = m.top.findNode("label")
end sub

sub onItemContent()
    content = m.top.itemContent
    if content = invalid then return
    m.label.text = content.TITLE
    m.icon.uri   = content.HDGRIDPOSTERURL
end sub

sub onFocusPercent()
    m.focusBg.opacity = m.top.focusPercent
end sub
