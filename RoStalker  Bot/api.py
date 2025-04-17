import requests
import json
import html
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import time

newAccountBonus = 5
with open('config.json', 'r') as file:
    config = json.load(file)

rosecurity = config.get(".ROBLOSECURITY")
webhookurl = config.get("WebhookURL")

class RobloxAPI:
    def __init__(self, db_file_path='db.json', code_file_path='codes.json'):
        self.DB_FILE_PATH = db_file_path
        self.CODE_FILE_PATH = code_file_path
    
    def format_timestamp(self, timestamp):
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
        
        unix_timestamp = int(dt.timestamp())
        
        discord_timestamp = f"<t:{unix_timestamp}:F>"
        
        return discord_timestamp
    
    def rbxtracker(self):
        current_time = datetime.now()
        modified_time = current_time - timedelta(hours=6)
        formatted_time = modified_time.strftime("%m/%d/%Y %H:%M:%S")
        rbx_event_tracker = f"CreateDate={formatted_time}"
        return rbx_event_tracker

    def last_online(self, uid):
        r = json.loads(requests.post(f"https://presence.roblox.com/v1/presence/users", json={"userIds":[str(uid)]}, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36"}, cookies={"rbx-ip2":"1","RBXEventTrackerV2":f"{self.rbxtracker}&rbxid=7014232136",".ROBLOSECURITY":rosecurity}).text)
        r2 = json.loads(requests.post(f"https://presence.roblox.com/v1/presence/last-online", json={"userIds":[str(uid)]}).text)
        upt = r['userPresences'][0]["userPresenceType"]
        if upt == 0:
            upt = "Offline"
        elif upt == 1:
            upt = "Online"
        elif upt == 2:
            upt = "In Game"
        elif upt == 3:
            upt = "In Studio"
        elif upt == 4:
            upt = "Hidden/Invisible"
        return upt, self.format_timestamp(r2['lastOnlineTimestamps'][0]['lastOnline']), r['userPresences'][0]['lastLocation'], r['userPresences'][0]['placeId'], r['userPresences'][0]['gameId'] 
    
    def check_validity(self, uid):
        if requests.get(f"https://users.roblox.com/v1/users/{uid}").status_code == 200:
            r = json.loads(requests.get(f"https://users.roblox.com/v1/users/{uid}").text)
            created = self.format_timestamp(r['created'])
            return 200, r['displayName'], r['name'], created, r['isBanned']
        else:
            return 404
    
    def find_games(self, uid):
        r = requests.get(f'https://badges.roblox.com/v1/users/{uid}/badges?sortOrder=Desc')

        npc = json.loads(r.text)['nextPageCursor']
        games = set()
        try:
            for item in json.loads(r.text)['data']:
                games.add(item['awarder']['id'])
            if npc:
                r = requests.get(f'https://badges.roblox.com/v1/users/{uid}/badges?sortOrder=Desc?nextPageCursor={npc}')
                for item in json.loads(r.text)['data']:
                    games.add(item['awarder']['id'])
            return games
        except:
            pass

    def get_followers(self, uid):
        r = requests.get(f"https://friends.roblox.com/v1/users/{uid}/followers/count").text
        return json.loads(r)['count']

    def get_following(self, uid):
        r = requests.get(f"https://friends.roblox.com/v1/users/{uid}/followings/count").text
        return json.loads(r)['count']

    def username_to_uid(self, username):
        r = requests.post(f"https://users.roblox.com/v1/usernames/users", json={"usernames":[str(username)],"excludeBannedUsers":False}).text
        if json.loads(r)['data'][0]['id']:
            return json.loads(r)['data'][0]['id']
        else:
            return 404

    def get_friends(self, uid):
        r = requests.get(f"https://friends.roblox.com/v1/users/{uid}/friends").text
        return json.loads(r)['data']
    
    def get_user_details(self, uid):
        r = requests.get(f"https://users.roblox.com/v1/users/{uid}").text
        user_info = json.loads(r)
        return f"{user_info['displayName']} (@{user_info['name']}) | ID: {uid}"
    
    def find_common_games(self, uid):
        user_games = self.find_games(uid)
        friends = self.get_friends(uid)
        common_games = {}
        
        for friend in friends:
            friend_id = friend['id']
            friend_games = self.find_games(friend_id)
            try:
                common = user_games.intersection(friend_games)
                if common:
                    friend_details = self.get_user_details(friend_id)
                    common_games[friend_details] = common
            except:
                continue
        
        return common_games
    
    def game2name(self, gid):
        al = requests.get(f'https://roblox.com/games/{gid}').text
        name = al[al.find('<title>') + 7 : al.find('</title>')]
        name = html.unescape(name)
        return name[:-9]
    
    def load_data(self):
        try:
            with open(self.DB_FILE_PATH, 'r') as file:
                data = json.load(file)
                return data.get("data", [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {self.DB_FILE_PATH}")
            return []
    
    def load_codes(self):
        try:
            with open(self.CODE_FILE_PATH, 'r') as file:
                data = json.load(file)
                return data.get("codes", [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {self.CODE_FILE_PATH}")
            return []
    
    def save_codes(self, data):
        try:
            with open(self.CODE_FILE_PATH, 'w') as file:
                json.dump({"codes": data}, file, indent=4)
        except Exception as e:
            print(f"Error saving data to {self.CODE_FILE_PATH}: {e}")

    def save_data(self, data):
        try:
            with open(self.DB_FILE_PATH, 'w') as file:
                json.dump({"data": data}, file, indent=4)
        except Exception as e:
            print(f"Error saving data to {self.DB_FILE_PATH}: {e}")
    
    def use_code(self, duid, code):
        duid = int(duid)
        data = self.load_codes()
        
        for item in data:
            if item['Name'] == code:
                if duid in item.get('Used', []):
                    return 400, None
                if item['UsesLeft'] > 0:
                    amount = item['Amount']
                    item['UsesLeft'] -= 1
                    item['Used'].append(duid)
                    self.save_codes(data)
                    return 200, amount
                else:
                    return 404, None
        return 404, None
        
    def create_user(self, duid):
        duid = int(duid)
        data = self.load_data()
        if any(user['UID'] == duid for user in data):
            return 400
        else:
            data.append({"UID": duid, "Balance": newAccountBonus})
            self.save_data(data)
            return 200
    
    def top_up_user(self, duid, balance_to_add):
        data = self.load_data()
        user_found = False
        for user in data:
            if user['UID'] == duid:
                user['Balance'] += balance_to_add
                user_found = True
                break
        if user_found:
            self.save_data(data)
            return 200
        else:
            return 404
    
    def get_balance(self, duid):
        data = self.load_data()
        for user in data:
            if user['UID'] == duid:
                return user['Balance']
        return "err"
    
    def decrease_balance(self, duid):
        data = self.load_data()
        user_found = False
        for user in data:
            if user['UID'] == duid:
                if user['Balance'] > 0:
                    user['Balance'] -= 1
                    user_found = True
                else:
                    return 403
                break
        if user_found:
            self.save_data(data)
            return 200
        else:
            return 404
    
    def getimg(self, uid):
        r = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={uid}&size=720x720&format=Png&isCircular=true")
        return json.loads(r.text)['data'][0]['imageUrl']

    def sendwhook(self, uid, duid):
        img = self.getimg(uid)
        json = {
            "content": None,
            "embeds": [
                {
                "title": "Search",
                "description": f"<@{duid}> searched for {self.get_user_details(uid)}",
                "color": 8582233,
                "author": {
                    "name": "RoStalker | Search"
                },
                "footer": {
                    "text": f"RoStalker | User Balance: {self.get_balance(duid)}"
                },
                "thumbnail": {
                    "url": f"{img}"
                }
                }
            ],
            "username": "RoStalker",
            "avatar_url": "https://cdn.discordapp.com/avatars/1194376439085150340/cefdc8f21b5b96b72150464b18cc5db6.png?size=1024",
            "attachments": []
            }
        requests.post(webhookurl, json=json)

