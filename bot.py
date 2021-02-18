# imports
from mcstatus import MinecraftServer # package for finding which players are online
import discord # discord.py package for discord bot connection
from discord.ext.commands import Bot


# getting the information from config.txt
Config = open("./config.txt")
IP = Config.readline()[9:].strip()
print("Server IP address: " + IP)
PORT = int(Config.readline()[11:].strip())
print("Server port: " + str(PORT))
QPORT = int(Config.readline()[10:].strip())
print("Server query port: " + str(QPORT))
BOTPREFIX = Config.readline()[10:].strip()
print("Discord bot prefix: " + BOTPREFIX)
BOTTOKEN = Config.readline()[9:].strip()
print("Got bot token")
CHANNELID = Config.readline()[16:]
print("Currently online channel ID: " + CHANNELID)
Config.close()

# declaring the client object
client = Bot(command_prefix = BOTPREFIX)

# removing the default help command so that a better one can be made using embeds
client.remove_command("help")

# changing the bot's status to "Listening to $help" and printing that the bot has logged in without any issues
@client.event
async def on_ready():
    ListeningTo = discord.Activity(type=discord.ActivityType.listening, name="$help")
    await client.change_presence(status=discord.Status.online, activity=ListeningTo)
    print('We have logged in as {0.user}'.format(client))


# ip command
@client.command(name = "ip")
async def ip(ctx):
    # creating embed
    IPEmbed = discord.Embed(
        colour = discord.Color.light_gray()
    )
    IPEmbed.set_author(name = f"Server IP: {IP}")

    # sending embed to current channel
    await ctx.send(embed = IPEmbed)

# playercount command
@client.command(name = "playercount")
async def playercount(ctx):
    # getting the number of players online from mcstatus
    server = MinecraftServer(IP, PORT)
    status = server.status()

    # creating the embed
    CountEmbed = discord.Embed(
        colour = discord.Colour.light_gray()
    )
    CountEmbed.set_author(name = "The server has {0} players online".format(status.players.online))
    
    # sedning the embed in the channel which the command was run in
    await ctx.send(embed = CountEmbed)


# playerlist command
@client.command(name = "playerlist")
async def playerlist(ctx):
    # crating the query object
    serverquery = MinecraftServer(IP, QPORT)
    query = serverquery.query()
    
    # creating the embed
    ListEmbed = discord.Embed(
        colour = discord.Colour.light_gray()
    )
    ListEmbed.set_author(name = "The server has the following players online: {0}".format(", ".join(query.players.names)))

    # sending the embed in the channel the command was run in
    await ctx.send(embed = ListEmbed)


# online command
@client.command(name = "online")
async def online(ctx):
    # declaring the objects for the minecraft server
    server = MinecraftServer(IP, PORT)
    status = server.status()
    serverquery = MinecraftServer(IP, QPORT)
    query = serverquery.query()
    
    Embed = discord.Embed(
            colour = discord.Colour.light_gray(),
            description = "The server has the following players online: {0}".format(", ".join(query.players.names))
        )
    Embed.set_author(name = "The server has {0} players online".format(status.players.online))

    await ctx.send(embed = Embed)


# help command
@client.command(name = "help")
async def help(ctx):
    # creating the embed for help
    HelpEmbed = discord.Embed(
        colour = discord.Colour.light_gray()
    )
    HelpEmbed.set_author(name = "discord.mc bot help")
    HelpEmbed.add_field(name = BOTPREFIX + "online", value = "Lists how many, and what players are on the server")
    HelpEmbed.add_field(name = BOTPREFIX + "playerlist", value = "Lists what players are online the server")
    HelpEmbed.add_field(name = BOTPREFIX + "playercount", value = "Shows how many players are currently online")
    HelpEmbed.set_footer(text = "Bot programmed by https://github.com/mattmoody05")

    # sends the embed in the channel that the command was run in
    await ctx.send(embed = HelpEmbed)


# running the bot using the bot token
client.run(BOTTOKEN)