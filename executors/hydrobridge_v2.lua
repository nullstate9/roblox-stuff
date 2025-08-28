--[[
      created by 109dg

USAGE:
getgenv().hydrobridge - where everything is stored

getgenv().hydrobridge.getclients() - get clients table
getgenv().hydrobridge.execute(username: string, script: string) - runs command on specific client 

getgenv().hydrobridge.getclients() will return a table that looks like this:
{            
 {clientObject},            
 {clientObject},
 ...
}

clientObject = {
      username = string,
      gameId = number,
      jobId = string,
      lastCommandId = number,
      commands = table,
      lastHeartbeat = number
}
--]]

local fileName = "hydrobridge.json"
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer

getgenv().hydrobridge = {}

local data = {}
if isfile(fileName) then
    local content = readfile(fileName)
    local success, parsed = pcall(function()
        return HttpService:JSONDecode(content)
    end)
    if success and typeof(parsed) == "table" then
        data = parsed
    end
end

table.insert(data, {
    username = LocalPlayer.Name,
    gameId = game.PlaceId,
    jobId = game.JobId,
    lastCommandId = 0,
    commands = {},
    lastHeartbeat = os.time()
})
writefile(fileName, HttpService:JSONEncode(data))

local function saveclients(clients)
    local encoded = HttpService:JSONEncode(clients)
    writefile(fileName, encoded)
end

getgenv().hydrobridge.getclients = function()
    if not isfile(fileName) then 
        return {} 
    end

    local content = readfile(fileName)
    local success, parsed = pcall(function()
        return HttpService:JSONDecode(content)
    end)

    if success and typeof(parsed) == "table" then
        return parsed
    else
        warn("[HYDROBRIDGE] Failed to parse hydrobridge.json")
        return {}
    end
end

getgenv().hydrobridge.execute = function(username, scriptStr)
    local clients = getgenv().hydrobridge.getclients()
    
    for i, client in ipairs(clients) do
        if client.username == username then
            client.commands = client.commands or {}
            
            local lastId = 0
            for _, cmd in ipairs(client.commands) do
                if cmd.id > lastId then
                    lastId = cmd.id
                end
            end
            
            table.insert(client.commands, {
                id = lastId + 1,
                script = scriptStr,
                executed = false
            })
            
            clients[i] = client
            saveclients(clients)
            return true
        end
    end
    
    warn("[HYDROBRIDGE] Client with username '" .. username .. "' not found")
    return false
end

local function executeLocal(script, commandId)
    print("[HYDROBRIDGE] Executing command on client: " .. LocalPlayer.Name)
    
    local func, err = loadstring(script)
    if func then
        local success, runErr = pcall(func)
        if not success then
            warn("[HYDROBRIDGE] Script error: " .. runErr)
            return false
        else
            local clients = getgenv().hydrobridge.getclients()
            for i, client in ipairs(clients) do
                if client.username == LocalPlayer.Name then
                    client.lastCommandId = commandId
                    if client.commands then
                        for _, cmd in ipairs(client.commands) do
                            if cmd.id == commandId then
                                cmd.executed = true
                                break
                            end
                        end
                    end
                    clients[i] = client
                    saveclients(clients)
                    break
                end
            end
            return true
        end
    else
        warn("[HYDROBRIDGE] Loadstring error: " .. tostring(err))
        return false
    end
end

spawn(function()
    while true do
        local clients = getgenv().hydrobridge.getclients()
        local now = os.time()

        local updated = false
        for i, client in ipairs(clients) do
            if client.username == LocalPlayer.Name then
                client.lastHeartbeat = now
                clients[i] = client
                updated = true
                break
            end
        end

        local cleanedClients = {}
        for _, client in ipairs(clients) do
            if client.lastHeartbeat and now - client.lastHeartbeat <= 5 then
                table.insert(cleanedClients, client)
            end
        end

        if updated or #cleanedClients ~= #clients then
            saveclients(cleanedClients)
        end

        for _, client in ipairs(cleanedClients) do
            if client.username == LocalPlayer.Name and client.commands then
                for _, command in ipairs(client.commands) do
                    if (not command.executed) and command.id > (client.lastCommandId or 0) then
                        executeLocal(command.script, command.id)
                    end
                end
            end
        end

        task.wait(1)
    end
end)
