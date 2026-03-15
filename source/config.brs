function getServerUrl() as String
    return "http://0.0.0.0:6567"
end function

function getApiKey() as String
    return "myapikey"
end function

' URL-encode each segment of a slash-separated path.
' BrightScript's roUrlTransfer.Escape() encodes a single string component.
function urlEncodePath(path as String) as String
    transfer = CreateObject("roUrlTransfer")
    parts    = path.Split("/")
    encoded  = []
    for each part in parts
        encoded.Push(transfer.Escape(part))
    end for
    return encoded.Join("/")
end function
