import discord
import rebrick
from discord.ext import commands

#  commands start with % to invoke the bot
client = commands.Bot(command_prefix="%")

#Open a file that contains the Rebrickable API key, Rebrickable token,
#Discord token,and login credentials for Rebrickable
credentials = open("credentials.txt", "rt")
for line in credentials:
    x = line.split(',')

key = x[0]
brick_token = x[1]
discord_token = x[2]
username = x[3]
password = x[4]

#invoke the rebrick wrapper (made by https://github.com/xxao)
rb = rebrick.Rebrick(key, brick_token, silent=True)
rb.login(username, password)


@client.event
async def on_ready():
    print("LeGrep is ready to search!")


#show the user's list
@client.command()
async def ul(ctx):

    setlist = rb.get_users_setlists()
    user_sets = rb.get_users_sets()

    embed = discord.Embed(
        title=f"Here is the inventory list for user {username}:",
        color=discord.Color.dark_green()
    )
    embed.set_thumbnail(url='https://github.com/nicolielloj/LeGrep-Discord-Bot/blob/main/bot_img.PNG?raw=true')

    embed.add_field(
        name='Set list',
        value=setlist,
        inline=False
    )

    embed.add_field(
        name="user setlist",
        value=user_sets,
        inline=False
    )
    await ctx.send(embed=embed)


@client.command()
async def gs(ctx, arg):
    # get set info
    url = rb.get_set(arg).url
    set_name = rb.get_set(arg).name
    theme = rb.get_set_themes(arg)[0].name
    pieces = rb.get_set(arg).pieces
    figs = rb.get_set_minifigs(arg)
    alt = rb.get_set_alternates(arg)
    img = rb.get_set(arg).img_url

    embed = discord.Embed(
        title="Here is your search result:",
        color=discord.Color.dark_blue()
    )
    embed.set_image(url=img)
    embed.add_field(
        name='URL',
        value=url,
        inline=False
    )
    embed.add_field(
        name='Set Name',
        value=set_name,
        inline=True
    )
    embed.add_field(
        name="Theme",
        value=theme,
        inline=True
    )
    embed.add_field(
        name="Pieces",
        value=pieces,
        inline=True
    )
    embed.add_field(
        name='Minifigs',
        value=figs,
        inline=False
    )
    embed.add_field(
        name="Alt Build",
        value=alt,
        inline=True
    )
    await ctx.send(embed=embed)

#overrides the default help command
client.remove_command('help')

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="LeGrep Commands",
        description='',
        color=discord.Color.dark_orange()
    )
    embed.set_thumbnail(url='https://github.com/nicolielloj/LeGrep-Discord-Bot/blob/main/bot_img.PNG?raw=true')
    embed.add_field(
        name='`%gs`',
        value="Get Set: fetch info about a LEGO set's name, theme, pieces, minifigure for the list, & Alternate builds",
        inline=True
    )
    embed.add_field(
        name='`%ul`',
        value="User List: Display the signed in user's set list",
        inline=True
    )
    await ctx.send(embed=embed)


#Power on the Bot
client.run(discord_token)

