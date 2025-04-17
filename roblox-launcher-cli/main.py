import requests
import json
import time
import random
import os



def joinGame(gameID):
    with open('config.json', 'r') as f:
        ROBLOSECURITY = json.loads(f.read())['.ROBLOSECURITY']
        if ROBLOSECURITY == "":
            print("[!] Roblox Cookie not found.")
            return
    session = requests.Session()

    session.cookies.set(".ROBLOSECURITY", ROBLOSECURITY)

    r = session.post("https://auth.roblox.com/v2/signup")
    csrf = r.headers.get('x-csrf-token')

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en;q=0.9",
        "Origin": "https://www.roblox.com/",
        "Referer": "https://www.roblox.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "X-Csrf-Token": csrf
    }

    r = session.get('https://auth.roblox.com/v1/client-assertion', headers=headers)
    clientAssertion = json.loads(r.text)['clientAssertion']

    r = session.get('https://roblox.com/home', headers=headers)
    browserTracker = r.cookies.get('RBXEventTrackerV2').split('browserid=')[1]

    payload = {
        "clientAssertion": clientAssertion
    }
    r = session.post('https://auth.roblox.com/v1/authentication-ticket/', headers=headers, json=payload)
    authTicket = r.headers.get('Rbx-Authentication-Ticket')

    r = session.get(f"https://games.roblox.com/v1/games/{gameID}/servers/Public?cursor=&sortOrder=Desc&excludeFullGames=false")
    data = json.loads(r.text)['data']

    available_games = [game for game in data if (game['maxPlayers'] - game['playing']) >= 3]

    if available_games:
        gameItem = random.choice(available_games)
    else:
        gameItem = {"id": None}

    jobID = gameItem['id']
    currtime = int(time.time())


    if jobID == None:
        url = f"roblox-player:1+launchmode:play+gameinfo:{authTicket}+launchtime:{currtime}+placelauncherurl:https%3A%2F%2Fwww.roblox.com%2FGame%2FPlaceLauncher.ashx%3Frequest%3DRequestGameJob%26browserTrackerId%3D{browserTracker}%26placeId%3D{gameID}%26isPlayTogetherGame%3Dfalse%26joinAttemptOrigin%3DServerListJoin+browsertrackerid:{browserTracker}+robloxLocale:en_us+gameLocale:en_us+channel:"
    else:
        url = f"roblox-player:1+launchmode:play+gameinfo:{authTicket}+launchtime:{currtime}+placelauncherurl:https%3A%2F%2Fwww.roblox.com%2FGame%2FPlaceLauncher.ashx%3Frequest%3DRequestGameJob%26browserTrackerId%3D{browserTracker}%26placeId%3D{gameID}%26gameId%3D{jobID}%26isPlayTogetherGame%3Dfalse%26joinAttemptId%3D{jobID}%26joinAttemptOrigin%3DServerListJoin+browsertrackerid:{browserTracker}+robloxLocale:en_us+gameLocale:en_us+channel:"
    os.system(f'xdg-open "{url}"') # change xdg-open to whatever

gameId = int(input("Game ID: https://roblox.com/games/"))
joinGame(gameId)



