import os
import env
import nextcord
from nextcord.ext import commands

# Variables
token_file = open("token.auth", "r")
token = token_file.read()

### DEBUG - REMOVE BEFORE PRODUCTIVE RELEASE!!!
testServerID = env.server_id
### DEBUG - REMOVE BEFORE PRODUCTIVE RELEASE!!!

intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

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
