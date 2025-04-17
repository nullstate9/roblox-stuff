# New Functions

I wanted to add more functions to the `crypt` library for Roblox Executors, as there were no implementations for HMACSHA256 or JSON Web Tokens (JWT). 

```lua
crypt.hmac_encode(key, message)

-- Example
local hmac_bin = crypt.hmac_encode("MyKey123", "Hello There!")
local hmac_b64 = base64_encode(hmac)
print(hmac_b64)
-- Output: cYTg2wO6WVP9dRO1G5ksHouqqKBA24KYaEjSR0lEpCE=
```
Function Overview: A cryptographic function emulating HMACSHA256, used to securely verify the integrity and authenticity of data. I created this function for JSON Web Tokens.

Returns: 256-bit Binary Digest

To convert to human-readable, you can just encode it to base64.

```lua
crypt.jwt_encode(key, payload)

-- Example
local body = {name = "nullstate9", "userId": "123456"}
local jwt = crypt.jwt_encode("MyKey123", body)
print(jwt)

-- Output: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoibnVsbHN0YXRlOSIsInVzZXJJZCI6IjEyMzQ1NiJ9.Nb0RNM7QkvKb9u6EJaQmjqgAG1K1FW-XOzAsoHCUdZI
```
Function Overview: Encodes a Table as a JSON Web Token (JWT) (Using the HS256 algorithm)

Returns: JWT Token. Read about JWT Tokens [Here](https://jwt.io/introduction)

```lua
crypt.jwt_decode(key, token)

-- Example
local jwtToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoibnVsbHN0YXRlO..." -- See Above Output
local decoded_payload = crypt.jwt_decode("MyKey123", jwtToken)
-- Output: <table 0xffff1249214> -- table object
```
Function Overview: Decodes a JSON Web Token (JWT) by resigning the Header and Payload and comparing the signature with the signature within the JWT. 

Returns: Table (valid), "Invalid JWT Signature" (invalid)
