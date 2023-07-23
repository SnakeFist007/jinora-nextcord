import os
import logging
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from functions.helpers import parse_embed

## Variables
load_dotenv()

# * Intents & Bot initialization
intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, help_command=None)

# * Logging
logger = logging.getLogger("nextcord")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename="jinora-nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

## Events
# * ON STARTUP
@bot.event
async def on_ready():
    print("\n\tJinora#2184 is ready!")
    try:
        await bot.sync_application_commands()
        print("\tSynced global commands!\n")
    except Exception as e:
        print(e)
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="you <3"))


# * ON SERVER JOIN
@bot.event
async def on_guild_join(guild):
    print(f"Joined server {guild.id}!")

    # Send welcome message to system channel, if available
    if guild.system_channel is not None:
        em = parse_embed("database/embeds/welcome_embed.json")
        await guild.system_channel.send(embed=em)


# * ON SERVER LEAVE
@bot.event
async def on_guild_remove(guild):
    print(f"Left server {guild.id}!")



## * Main run function
def main():
    # Load extensions
    print("Loading modules... \n")
    for folder in os.listdir("cogs"):
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            bot.load_extension(f"cogs.{folder}.cog")
    
    # Start the bot
    bot.run(os.getenv("TOKEN"))

if __name__ == "__main__":
    main()
