# Roblox Terminal Launcher 

A simple Terminal-Based Game Launcher. Can be tweaked, i don't really care. 

(LINUX ONLY, READ BELOW FOR OTHER OPERATING SYSTEMS)

On the last line of the `joinGame()` function, I used "xdg-open" to open the roblox-player: link. 
This can be substituted for `start` (Windows) and `open` (macOS) I believe.

You could also probably make joining a server work, just add another argument for `joinGame()`, and replace the following code

FROM:
```py
available_games = [game for game in data if (game['maxPlayers'] - game['playing']) >= 3]

if available_games:
    gameItem = random.choice(available_games)
else:
    gameItem = {"id": None}
```

TO:
```py
gameItem = {"id": "YOUR_SERVER_ID_HERE"}
```
