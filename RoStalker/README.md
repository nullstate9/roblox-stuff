# RoStalker

RoStalker Source Code, since i don't maintain the bot anymore. 
A basic Discord bot to gain information on any ROBLOX account.

> [!WARNING]
> Due to changes in ROBLOX APIs, some features may be obsolete.

## Setup

1. **Upgrade your pip version**
```
pip install --upgrade pip
```

2. **Install required libraries**
```
pip install requests discord
```

3. **Setup your Config File**

- `Discord-Bot-Token`: Your Discord Bot Token

- `OwnerIDs`: Discord IDs of all the owners (must be integer)

- `.ROBLOSECURITY`: Required for the current playing game of a user, a throwaway roblox cookie is advised to be used

- `WebhookURL`: Discord webhook url for logging searches

4. **Commands**
```
/help - Displays the list of available commands.
/createuser - Creates a RoStalker account.
/redeem - Redeems a RoStalker promocode for credits.
/quicksearch - Searches for a Roblox Account, and provides brief information.
/search - Searches for a Roblox Account, and provides a full summary, including activity status, previously played games, games played with friends and more.
/getbalance - Returns your current RoStalker balance. Requires a RoStalker account.

OWNER Commands
/createuser - can force user creation
/getbalance - can get any user's balance
/topup - gives RoStalker tokens to any discord user (Must have Discord Server Administrator Permissions & in OwnerIDs config list.)
```
