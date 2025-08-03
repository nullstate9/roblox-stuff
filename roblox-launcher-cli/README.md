# Roblox Launcher CLI

Useful functions for automating server-joining, without the use of the ROBLOX Application.

**multi-platform**. It emulates the url-scheme `roblox-player://`, which can be opened with "start" for Windows, "open" for macOS or "xdg-open" for certain Linux Distributions.

Documentation within the script.


Required External Libraries: `requests`
Required In-Built Libraries: `json`, `time`, `random`, `typing`

`client.get_online_friends()` returns a list with dictionaries.

Example Dictionary:
```
{
"userPresence": {
  "UserPresenceType": "InGame",
    "UserLocationType": "Game",
    "lastLocation": "Game Name",
    "placeId": 12345678,
    "rootPlaceId": 12345678,
    "gameInstanceId": "ffffffff-eeee-dddd-cccc-ffffffff",
    "universeId": 123,
    "lastOnline": "YYYY-MM-DDTHH:MM:SS.000Z"
  },
  "id": 123456
},
```

