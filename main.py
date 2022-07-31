import nextcord
from discord import Intents
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands
import os
import env

# Variables
token_file = open("token.auth", "r")
token = token_file.read()

testServerID = env.server_id

intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
#bot.remove_command("help")

# Events
@bot.event
async def on_ready():
    print("Lene-Bot is ready!")
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="you <3"))

# Load extensions
for folder in os.listdir("cogs"):
    if os.path.exists(os.path.join("cogs", folder, "cog.py")):
        bot.load_extension(f"cogs.{folder}.cog")

# Run
bot.run(token)
