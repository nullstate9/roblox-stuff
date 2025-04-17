from api import RobloxAPI
import discord
from discord import app_commands
from discord.ext import commands
version = "BETA 5.1"

with open('config.json', 'r') as file:
    config = json.load(file)


api = RobloxAPI()
TOKEN = config.get('Discord-Bot-Token')

OWNER_USERIDS = config.get('OwnerIDs', [])

emoji="<a:loading:1258493187404726362>"

bot = commands.Bot(command_prefix="rs!", intents = discord.Intents.all(), help_command=None)

@bot.command()
async def sync(ctx):
    if ctx.author.id in OWNER_USERIDS:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
        print("Synced")
    else:
        pass

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"/search"))
    print(f"ROSTALKER 2 UP")


async def check_dm_enabled(user: discord.User) -> bool:
    try:
        await user.send("")
        return True
    except discord.Forbidden:
        return False   
    except discord.HTTPException:
        return True

@bot.tree.command(name="help", description="Lists available commands")
async def help(ctx: discord.Interaction):
    embed = discord.Embed(title="RoStalker Commands",
                  description=f"",
                  colour=0x82f459)

    embed.add_field(name="/help", value="Displays the list of available commands.", inline=False)
    embed.add_field(name="/createuser", value="Creates a RoStalker account.", inline=False)
    embed.add_field(name="/redeem", value="Redeems a RoStalker promocode for credits.", inline=False)
    embed.add_field(name="/quicksearch", value="Searches for a Roblox Account, and provides brief information.", inline=False)
    embed.add_field(name="/search", value="Searches for a Roblox Account, and provides a full summary, including activity status, previously played games, games played with friends and more.", inline=False)
    embed.add_field(name="/getbalance", value="Returns your current RoStalker balance. Requires a RoStalker account.", inline=False)
    
    embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
    await ctx.response.send_message(embed=embed)

@bot.tree.command(name="topup", description="Adds balance to user")
@app_commands.default_permissions(administrator=True)
async def addBal(ctx: discord.Interaction, amount: int, user: discord.User = None):
    await ctx.response.defer(ephemeral=True)
    if user is None:
        user = ctx.user
    f = api.get_balance(user.id)
    if ctx.user.id not in OWNER_USERIDS:
        embed = discord.Embed(title="Error",
            description="You do not have permission to set this!",
            colour=0xf45c51)
        
        embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
        await ctx.followup.send(embed=embed, ephemeral=True)
    else:
        if f == "err":
            embed = discord.Embed(title="Error",
                  description="User does not have a RoStalker Account!",
                  colour=0xf45c51)

            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed,ephemeral=True)
        else:
            api.top_up_user(user.id, amount)
            f = api.get_balance(user.id)
            embed = discord.Embed(title="Balance",
                  description=f"Added {amount} to User's Balance. Current Balance: {f}",
                  colour=0x82f459)

            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed, ephemeral=True)

    
@bot.tree.command(name="createuser", description="Creates a RoStalker 2 Account.")  
async def createuser(ctx: discord.Interaction, user: discord.User = None):
    await ctx.response.defer(ephemeral=True)
    if not user:
        user = ctx.user
    if ctx.user.id in OWNER_USERIDS:
        f = api.create_user(user.id)
        if f == 200:
            embed = discord.Embed(title="Success!",
                      description=f"Created RoStalker Account for {user.mention}!",
                      colour=0x82f459)
            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error",
                      description=f"{user.mention} already has a RoStalker Account!",
                      colour=0xf45c51)

            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed,ephemeral=True)
    else:
        if ctx.user.id == user.id:
            f = api.create_user(user.id)
            if f == 200:
                embed = discord.Embed(title="Success!",
                      description=f"Created RoStalker Account for you!",
                      colour=0x82f459)
                embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
                await ctx.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error",
                      description=f"You already have a RoStalker Account!",
                      colour=0xf45c51)

            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed,ephemeral=True)


@bot.tree.command(name="getbalance", description="Returns balance of a RoStalker 2 User.")  
async def getbal(ctx: discord.Interaction, user: discord.User = None):
    await ctx.response.defer(ephemeral=True)
    if user is None:
        user = ctx.user
    f = api.get_balance(user.id)
    if ctx.user.id == user.id:
        if f == "err":
            embed = discord.Embed(title="Error",
                      description="You do not have a RoStalker account! Create one by running /createuser",
                      colour=0xf45c51)

            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed,ephemeral=True)

        else:
            embed = discord.Embed(title="Balance",
                      description=f"Current Balance: {f}",
                      colour=0x82f459)

            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed, ephemeral=True)

    else:
        if ctx.user.id not in OWNER_USERIDS:
            embed = discord.Embed(title="Error",
                        description="You do not have permission to check this user's account!",
                        colour=0xf45c51)
            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed, ephemeral=True)
        else:
            if f == "err":
                embed = discord.Embed(title="Error",
                      description="User does not have a RoStalker Account!",
                      colour=0xf45c51)

                embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
                await ctx.followup.send(embed=embed,ephemeral=True)
            else:
                embed = discord.Embed(title="Balance",
                      description=f"Current User's Balance: {api.get_balance(user.id)}",
                      colour=0x82f459)

                embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
                await ctx.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="quicksearch", description="Gathers information on a Roblox User")  
async def quicksearch(ctx: discord.Interaction, userid: int=None, username: str=None):
    user = userid
    await ctx.response.defer(ephemeral=True)
    if not user and not username:
        embed = discord.Embed(title="Error",
                      description="You must provide either a Roblox User ID or Username!",
                      colour=0xf45c51)

        embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
        await ctx.followup.send(embed=embed,ephemeral=True)
        return

    if not user:
        user = api.username_to_uid(username)
        if user == 404:
            embed = discord.Embed(title="Error",
                      description="Username is invalid!",
                      colour=0xf45c51)

            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed,ephemeral=True)
            return
        f = api.check_validity(user)
        
        async def doSearch():
            statusembed = discord.Embed(title="Search",
                        description=f"Finding User {emoji}",
                        colour=0xf4ae2d)

            statusembed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.edit_original_response(embed=statusembed, view=None)

            status = api.last_online(user)
            infoembed = discord.Embed(title=f"{f[1]} (@{f[2]})",
                        url=f"https://roblox.com/users/{user}/profile",
                        description=f"",
                        colour=0x82f459)

            infoembed.add_field(name="Created", value=f[3], inline=False)
            infoembed.add_field(name="Banned", value=f[4], inline=True)
            infoembed.add_field(name="Status", value=f"{status[0]}", inline=True)
            infoembed.add_field(name="Last Online", value=status[1], inline=False)
                
            infoembed.set_author(name=f"Search: {f[1]} (@{f[2]})")
                
            statusembed = discord.Embed(title="Search",
                        description=f"Finding Friend Info. {emoji}",
                        colour=0xf4ae2d)

            statusembed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")

            await ctx.edit_original_response(content=f"", embed=statusembed)
                
            friendc = 0

            for friend in api.get_friends(user):
                try:
                    if friend['isOnline'] == True:
                        friendc += 1
                except:
                    continue

            infoembed.add_field(name="Friends",
                    value=f"{len(api.get_friends(user))}",
                    inline=True)

            infoembed.add_field(name="Followers",
                    value=f"{api.get_followers(user)}",
                    inline=True)

            infoembed.add_field(name="Following",
                    value=f"{api.get_following(user)}",
                    inline=True)
                
            infoembed.add_field(name="Online Friends",
                    value=f"{friendc}",
                    inline=True)

            statusembed = discord.Embed(title="Search",
                        description=f"Finding Icon {emoji}",
                        colour=0xf4ae2d)

            statusembed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            infoembed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.edit_original_response(content=f"", embed=statusembed)
            infoembed.set_thumbnail(url=f"{api.getimg(user)}") 

            await ctx.edit_original_response(embed=infoembed)
            api.sendwhook(user, ctx.user.id)
         
            
        class MyView(discord.ui.View):
            def __init__(self):
                super().__init__()

            @discord.ui.button(label="No, cancel.", style=discord.ButtonStyle.danger)
            async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                await ctx.edit_original_response(content=f"", view=None, embed=discord.Embed(title="Cancelled.",description="Search has been cancelled.", colour=0xf45c51))
                self.stop()

            @discord.ui.button(label="Yes, search.", style=discord.ButtonStyle.success)
            async def search_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                await doSearch()
                self.stop()

        embed = discord.Embed(
                title="Confirmation",
                description=f"**Are you sure you want to search for: {f[1]} (@{f[2]})?**",
                colour=0xf4ae2d
        )
        embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
        embed.set_thumbnail(url=f"{api.getimg(user)}")
        view = MyView()
        await ctx.followup.send(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="redeem", description="Redeems a RoStalker Promocode")
async def redeem(ctx: discord.Interaction, code: str):
    await ctx.response.defer(ephemeral=True)
    user = ctx.user.id
    f = api.use_code(user, code)
    if f[0] != 404:
        if f[0] == 200:
            api.top_up_user(user, f[1])
            embed = discord.Embed(
                title="Redeemed Code!",
                description=f"You have redeemed code: `{code}` for `{f[1]}` credits! Current Balance: {api.get_balance(ctx.user.id)}",
                colour=0x82f459
            )
            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed, ephemeral=True)
        elif f[0] == 400:
            embed = discord.Embed(
                title="Error",
                description="You have already used this code!",
                colour=0xf45c51
            )
            await ctx.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title="Error",
            description="Invalid Promocode!",
            colour=0xf45c51
        )
        await ctx.followup.send(embed=embed, ephemeral=True)
    
        
@bot.tree.command(name="search", description="Gathers full information on a Roblox User")  
async def search(ctx: discord.Interaction, userid: int=None, username: str=None):
    await ctx.response.defer(ephemeral=True)
    user = userid
    if not user and not username:
        embed = discord.Embed(title="Error",
                      description="You must provide either a Roblox User ID or Username!",
                      colour=0xf45c51)

        embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
        await ctx.followup.send(embed=embed,ephemeral=True)
        return

    if not user:
        user = api.username_to_uid(username)
        if user == 404:
            embed = discord.Embed(title="Error",
                      description="Username is invalid!",
                      colour=0xf45c51)

            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            await ctx.followup.send(embed=embed,ephemeral=True)
            return
    
    f = api.get_balance(ctx.user.id)
    if f == "err":
        embed = discord.Embed(title="Error",
                      description="You do not have a RoStalker account! Create one by running /createuser",
                      colour=0xf45c51)

        embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
        await ctx.followup.send(embed=embed,ephemeral=True)

    elif f > 0:
        f = api.check_validity(user)
        
        if f[0] != 404:

            if not await check_dm_enabled(ctx.user):

                embed = discord.Embed(
                    title="Error",
                    description="Please enable server DMs and try again.",
                    colour=0xf45c51
                )
                embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
                await ctx.followup.send(embed=embed, ephemeral=True)
                return
            
            async def doSearch():
                embedList = []
                statusembed = discord.Embed(title="Search",
                        description=f"Finding User {emoji}",
                        colour=0xf4ae2d)

                statusembed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
                await ctx.edit_original_response(embed=statusembed, view=None)

                status = api.last_online(user)

                statusembed = discord.Embed(title="Search",
                        description=f"Finding Recent Games {emoji}",
                        colour=0xf4ae2d)

                statusembed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")

                await ctx.edit_original_response(content=f"", embed=statusembed)
                gamestr = ""
                for game in api.find_games(user):
                    try:
                        gamestr += f"- [{api.game2name(game)}](https://roblox.com/games/{game})\n"
                    except:
                        continue


                usrgamedetails = ""
                if status[3]:
                    usrgamedetails = f"\nGame: [{status[2]}](https://roblox.com/games/{status[3]})\nServer ID: {status[4]}"

                infoembed = discord.Embed(title=f"{f[1]} (@{f[2]})",
                            url=f"https://roblox.com/users/{user}/profile",
                            description=f"",
                            colour=0x82f459)

                infoembed.add_field(name="Created", value=f[3], inline=False)
                infoembed.add_field(name="Banned", value=f[4], inline=True)
                infoembed.add_field(name="Status", value=f"{status[0]}{usrgamedetails}", inline=True)
                infoembed.add_field(name="Last Online", value=status[1], inline=False)
                infoembed.add_field(name="Last Known Played Games", value=gamestr, inline=False)
                
                infoembed.set_author(name=f"Search: {f[1]} (@{f[2]})")
                
                statusembed = discord.Embed(title="Search",
                        description=f"Finding Friend Info. This may take a while {emoji}",
                        colour=0xf4ae2d)

                statusembed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")

                await ctx.edit_original_response(content=f"", embed=statusembed)
                
                frienddetails = ""
                friendc = 0

                for friend in api.get_friends(user):
                    try:
                        if friend['isOnline'] == True:
                            friendc += 1
                            r = api.last_online(friend['id'])
                            try:
                                if r[3]:
                                    frienddetails += f"[{api.get_user_details(friend['id'])}](https://roblox.com/users/{friend['id']}/profile)\n"
                            except:
                                continue
                    except:
                        continue

                
                infoembed.add_field(name="Friends",
                    value=f"{len(api.get_friends(user))}",
                    inline=True)

                infoembed.add_field(name="Followers",
                    value=f"{api.get_followers(user)}",
                    inline=True)

                infoembed.add_field(name="Following",
                    value=f"{api.get_following(user)}",
                    inline=True)
                
                infoembed.add_field(name="Online Friends",
                    value=f"{friendc}",
                    inline=True)

                statusembed = discord.Embed(title="Search",
                        description=f"Finding Icon {emoji}",
                        colour=0xf4ae2d)

                statusembed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")

                await ctx.edit_original_response(content=f"", embed=statusembed)
                infoembed.set_thumbnail(url=f"{api.getimg(user)}")

                statusembed = discord.Embed(title="Search",
                        description=f"Finding Friend Game Status. This may take a while {emoji}",
                        colour=0xf4ae2d)

                statusembed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")

                await ctx.edit_original_response(content=f"", embed=statusembed)

                common_games = api.find_common_games(user)

                embedList.append(infoembed)

                info2embed = discord.Embed(title=f"",
                            description=f"**Friend Game Similarities**",
                            colour=0x82f459)
                
                info2embed2 = discord.Embed(title=f"",
                            description=f"**Friend Game Similarities**",
                            colour=0x82f459)
                
                fallback = False
                c = 0 
                d = 0
                for friend_details, games in common_games.items():
                    gamestr = ""
                    for game in games:
                        c += 1
                        try:
                            gamestr += f"[{api.game2name(game)}](https://roblox.com/games/{game})\n"
                        except:
                            continue
                    d += 1
                    if d < 24:
                        info2embed.add_field(name=f"{friend_details}",
                            value=f"{gamestr}",
                            inline=False)
                    else:
                        if not fallback:
                            fallback = True
                        info2embed2.add_field(name=f"{friend_details}",
                            value=f"{gamestr}",
                            inline=False)

                embedList.append(info2embed)
                if fallback:
                    embedList.append(info2embed2)

                if c == 0:
                    info2embed = discord.Embed(title=f"",
                            description=f"**Friend Game Similarities**\nNone",
                            colour=0x82f459)

                
                
                frienddetails = ""

                if not frienddetails:
                    frienddetails = "None"
                
                info3embed = discord.Embed(title=f"",
                            description=f"",
                            colour=0x82f459)

                info3embed.add_field(name="Joinable friends",
                    value=f"{frienddetails}",
                    inline=False)
                
                api.decrease_balance(ctx.user.id)
                info3embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version} | Balance: {api.get_balance(ctx.user.id)}\nSome info may be invalid/outdated.")

                embedList.append(info3embed)

                statusembed = discord.Embed(title="Search Complete!",
                        description=f"Search results for {f[1]} (@{f[2]}) have been DMed to you.",
                        colour=0x82f459)

                statusembed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version} | Remaining Balance: {api.get_balance(ctx.user.id)}")

                await ctx.edit_original_response(content=f"", embed=statusembed)
                try:
                    await ctx.user.send(embeds=embedList)
                except discord.HTTPException:
                    for embed in embedList:
                        await ctx.user.send(embed=embed)
                        
                api.sendwhook(user, ctx.user.id)
                
            class MyView(discord.ui.View):
                def __init__(self):
                    super().__init__()

                @discord.ui.button(label="No, cancel.", style=discord.ButtonStyle.danger)
                async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    await ctx.edit_original_response(content=f"", view=None, embed=discord.Embed(title="Cancelled.",description="Search has been cancelled.", colour=0xf45c51))
                    self.stop()

                @discord.ui.button(label="Yes, search.", style=discord.ButtonStyle.success)
                async def search_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    await doSearch()
                    self.stop()

            embed = discord.Embed(
                title="Confirmation",
                description=f"**Are you sure you want to search for: {f[1]} (@{f[2]})?**",
                colour=0xf4ae2d
            )
            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            embed.set_thumbnail(url=f"{api.getimg(user)}")
            view = MyView()
            await ctx.followup.send(embed=embed, view=view, ephemeral=True)


        else:
            embed = discord.Embed(title="Error",
                      description="Invalid User ID!",
                      colour=0xf45c51)

            embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
            embed.set_author(name=f"RoStalker")

            await ctx.followup.send(embed=embed,ephemeral=True)
    else:
        embed = discord.Embed(title="Error",
                      description="You do not have enough funds to complete this search!",
                      colour=0xf45c51)
        embed.set_footer(text=f"RoStalker 2 by @2killq | Version: {version}")
        embed.set_author(name=f"RoStalker")

        await ctx.followup.send(embed=embed,ephemeral=True)


bot.run(TOKEN)
