crypt.hmac_encode = function(key, message)
    -- Necessary Local Functions
    local function hex_decode(hex)
        local str = ""
        for i = 1, #hex - 1, 2 do
            local byte = tonumber(hex:sub(i, i + 1), 16)
            str = str .. string.char(byte)
        end
        return str
    end
    
    local function to_bytes(str)
        local bytes = {}
        for i = 1, #str do
            bytes[i] = str:byte(i)
        end
        return bytes
    end
    
    local function from_bytes(bytes)
        local chars = {}
        for i = 1, #bytes do
            chars[i] = string.char(bytes[i])
        end
        return table.concat(chars)
    end
    
    local function xor_bytes(a, b)
        local result = {}
        for i = 1, #a do
            result[i] = bit32.bxor(a[i], b[i])
        end
        return result
    end
    local block_size = 64
    
    if #key > block_size then
        key = crypt.hash(key, "sha256")
        key = hex_decode(key)
    end
    
    if #key < block_size then
        key = key .. string.rep("\0", block_size - #key)
    end
    
    local key_bytes = to_bytes(key)
    local ipad = xor_bytes(key_bytes, to_bytes(string.rep(string.char(0x36), block_size)))
    local opad = xor_bytes(key_bytes, to_bytes(string.rep(string.char(0x5c), block_size)))
    
    local inner_data = from_bytes(ipad) .. message
    local inner_hash = crypt.hash(inner_data, "sha256")
    local inner_bytes = hex_decode(inner_hash)
    
    local outer_data = from_bytes(opad) .. inner_bytes
    local outer_hash = crypt.hash(outer_data, "sha256")
    local final_bytes = hex_decode(outer_hash)
    
    return final_bytes
end

crypt.jwt_encode = function(key, payload)
    local HttpService = game:GetService("HttpService") -- Required for JSONEncode()

    local function base64url_encode(data) -- Formatting base64 encoding to URL-safe base64
        local b64 = base64_encode(data)
        return b64:gsub("+", "-"):gsub("/", "_"):gsub("=", "")
    end

    -- Required headers for JWT Tokens.
    local header = { 
        alg = "HS256",
        typ = "JWT"
    }

    -- Segments for JWT Token
    local encHeader = base64url_encode(HttpService:JSONEncode(header))
    local encPayload = base64url_encode(HttpService:JSONEncode(payload))
    local hpconcat = encHeader .. "." .. encPayload

    -- Creating the final segment (Signature segment)
    local rawSig = crypt.hmac_encode(key, hpconcat)
    local encSig = base64url_encode(rawSig)

    -- Final Concatenation
    local token = hpconcat .. "." .. encSig
    return token
end

crypt.jwt_decode = function(key, token)
    local HttpService = game:GetService("HttpService")-- Required for JSONEncode() and JSONDecode()

    local function base64url_encode(data) -- Formatting base64 encoding to URL-safe base64
        local b64 = base64_encode(data)
        return b64:gsub("+", "-"):gsub("/", "_"):gsub("=", "")
    end

    local function base64url_decode(str) -- Opposite of base64url_encode()
        local padding = string.rep("=", (4 - (string.len(str) % 4)) % 4)
        local base64 = str:gsub("-", "+"):gsub("_", "/") .. padding
        return base64_decode(base64)
    end

    local encHeader, encPayload, encSig = string.match(token, "([^%.]+)%.([^%.]+)%.([^%.]+)") -- Regex for JWT Format Check
    
    if not encHeader or not encPayload or not encSig then -- If JWT Format is invalid
        return "Invalid JWT Signature"
    end

    -- Does not require Decoded Header so that has been omitted.
    local decodedPayload = base64url_decode(encPayload) -- Decoding JWT Payload
    
    local message = encHeader .. "." .. encPayload -- Concatenation

    local reSig = base64url_encode(crypt.hmac_encode(key, message)) -- Resigning header and payload
    
    if reSig == encSig then -- Comparing Resigned with JWT Signature
        return HttpService:JSONDecode(decodedPayload) -- Returning Table
    else
        return "Invalid JWT Signature"
    end
end
