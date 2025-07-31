--[[
      created by 109dg

USAGE:
getgenv().hydrobridge - where everything is stored

getgenv().hydrobridge.getclients() - get clients table
getgenv().hydrobridge.showclientnumbers() - shows the client number on each client
getgenv().hydrobridge.hideclientnumbers() - shows the client number on each client
getgenv().hydrobridge.addcommand(clientnumber, script) - runs command on specific client 


getgenv().hydrobridge.getclients() will return a table that looks like this
{            
 {clientObject},            
 {clientObject},
 ...
}

clientObject = {
      clientNumber = int,
      username = string,
      lastCommandId = int,
      commands = table,
      lastHeartbeat = float or int idk
}

you'll only need to know clientNumber and username, the last three are for hydrobridge

also the showclientnumbers() is probably susceptible to being detected by 
in-game anticheats because it creates a screengui in PlayerGui

]]--


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

local clientNumber = nil
for _, client in ipairs(data) do
    if client.username == LocalPlayer.Name then
        clientNumber = client.clientNumber
        break
    end
end

if not clientNumber then
    clientNumber = #data + 1
    table.insert(data, {
        clientNumber = clientNumber,
        username = LocalPlayer.Name,
        lastCommandId = 0,
        commands = {},
        lastHeartbeat = os.time()
    })
    writefile(fileName, HttpService:JSONEncode(data))
end

local function saveclients(clients)
    local encoded = HttpService:JSONEncode(clients)
    writefile(fileName, encoded)
end

getgenv().hydrobridge.getclients = function()
    if not isfile(fileName) then return {} end

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

getgenv().hydrobridge.addcommand = function(clientNum, scriptStr)
    local clients = getgenv().hydrobridge.getclients()
    for i, client in ipairs(clients) do
        if client.clientNumber == clientNum then
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
            print("[HYDROBRIDGE] Added command id " .. (lastId + 1) .. " for client " .. client.username)
            return
        end
    end
    warn("[HYDROBRIDGE] Client number " .. tostring(clientNum) .. " not found to add command")
end

getgenv().hydrobridge.fireclient = function(clientNum, scr, commandId)
    local clients = getgenv().hydrobridge.getclients()
    local targetClient = nil

    for _, client in ipairs(clients) do
        if client.clientNumber == clientNum then
            targetClient = client
            break
        end
    end

    if targetClient then
        if targetClient.username == LocalPlayer.Name then
            print("[HYDROBRIDGE] Executing command on client: " .. targetClient.username)
            local func, err = loadstring(scr)
            if func then
                local success, runErr = pcall(func)
                if not success then
                    warn("[HYDROBRIDGE] Script error: " .. runErr)
                else
                    if targetClient.commands then
                        for _, cmd in ipairs(targetClient.commands) do
                            if cmd.id == commandId then
                                cmd.executed = true
                                break
                            end
                        end
                    end

                    targetClient.lastCommandId = commandId

                    for i, c in ipairs(clients) do
                        if c.clientNumber == clientNum then
                            clients[i] = targetClient
                            break
                        end
                    end
                    saveclients(clients)
                end
            else
                warn("[HYDROBRIDGE] Loadstring error: " .. tostring(err))
            end
        end
    else
        warn("[HYDROBRIDGE] No client found with clientNumber " .. tostring(clientNum))
    end
end

getgenv().hydrobridge.showclientnumbers = function() 
    for _, client in ipairs(getgenv().hydrobridge.getclients()) do 
        local num = client.clientNumber 
        local scr = [[
            if game.Players.LocalPlayer.PlayerGui:FindFirstChild("hybridge") then 
                game.Players.LocalPlayer.PlayerGui:FindFirstChild("hybridge"):Destroy() 
            end
            local screenGui = Instance.new("ScreenGui", game.Players.LocalPlayer.PlayerGui)
            screenGui.Name = "hybridge" -- prob detected lel
            screenGui.ResetOnSpawn = false
            local textlabel = Instance.new("TextLabel", screenGui)
            textlabel.AnchorPoint = Vector2.new(1,1)
            textlabel.Size = UDim2.new(0,30,0,30)
            textlabel.Text = "]] .. tostring(num) .. [["
            textlabel.TextScaled = true 
            textlabel.Position = UDim2.new(1,-10,1,-10)
        ]]
        getgenv().hydrobridge.addcommand(num, scr)
    end 
end 

hydrobridge.hideclientnumbers = function() 
    for _, client in ipairs(getgenv().hydrobridge.getclients()) do 
        local num = client.clientNumber 
        local scr = [[
            local screenGui = game.Players.LocalPlayer.PlayerGui:FindFirstChild("hybridge")
            if screenGui then 
                screenGui:Destroy()
            end
        ]]
        getgenv().hydrobridge.addcommand(num, scr)
    end
end 

spawn(function()
    while true do
        local clients = getgenv().hydrobridge.getclients()
        local now = os.time()

        local updated = false
        for i, client in ipairs(clients) do
            if client.clientNumber == clientNumber then
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
            else
                -- client left
            end
        end

        if updated or #cleanedClients ~= #clients then
            saveclients(cleanedClients)
        end

        for _, client in ipairs(cleanedClients) do
            if client.clientNumber == clientNumber and client.commands then
                for _, command in ipairs(client.commands) do
                    if (not command.executed) and command.id > (client.lastCommandId or 0) then
                        getgenv().hydrobridge.fireclient(clientNumber, command.script, command.id)
                    end
                end
            end
        end

        task.wait(1)
    end
end)

