# New Functions

Proposed additions to the `crypt` library for Roblox Executors.

Unfortunately these were not implemented into sUNC as there is no demand for more functions such as this, and also it is vulnerable to being hooked. 

One way to circumvent this is by copying the functions as local functions. This, however, **may** be vulnerable to `getgc()` or `filtergc()`. 

## Functions Docs

### crypt.hmac_encode()
```lua
crypt.hmac_encode(key, message) -- Requires crypt.hash()

-- Example
local hmac_bin = crypt.hmac_encode("MyKey123", "Hello There!")
local hmac_b64 = base64_encode(hmac)
print(hmac_b64)
-- Output: cYTg2wO6WVP9dRO1G5ksHouqqKBA24KYaEjSR0lEpCE=
```
Function Overview: A cryptographic function emulating HMACSHA256, used to securely verify the integrity and authenticity of data. I created this function for JSON Web Tokens.

Returns: 256-bit Binary Digest

To convert to human-readable, you can just encode it to base64.

### crypt.jwt_encode()
```lua
crypt.jwt_encode(key, payload) -- Requires crypt.hmac_encode() and base64_encode()

-- Example
local body = {name = "nullstate9", "userId": "123456"}
local jwt = crypt.jwt_encode("MyKey123", body)
print(jwt)

-- Output: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoibnVsbHN0YXRlOSIsInVzZXJJZCI6IjEyMzQ1NiJ9.Nb0RNM7QkvKb9u6EJaQmjqgAG1K1FW-XOzAsoHCUdZI
```
Function Overview: Encodes a Table as a JSON Web Token (JWT) (Using the HS256 algorithm)

Returns: JWT Token. Read about JWT Tokens [Here](https://jwt.io/introduction)

### crypt.jwt_decode()
```lua
crypt.jwt_decode(key, token) -- Requires base64_encode() and base64_decode()

-- Example
local jwtToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoibnVsbHN0YXRlOSIsInVzZXJJZCI6IjEyMzQ1NiJ9.Nb0RNM7QkvKb9u6EJaQmjqgAG1K1FW-XOzAsoHCUdZI" -- See Above Output
local decoded_payload = crypt.jwt_decode("MyKey123", jwtToken)
-- Output: <table 0xffff1249214> -- table object
```
Function Overview: Decodes a JSON Web Token (JWT) by resigning the Header and Payload and comparing the signature with the signature within the JWT. 

Returns: Table (valid), "Invalid JWT Signature" (invalid)
