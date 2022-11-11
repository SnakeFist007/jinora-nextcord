import os
import shutil
import logging
import nextcord
from nextcord import application_command
from nextcord.ext import commands

## Variables
token_file = open("token.auth", "r")
token = token_file.read()

# Intents & Bot initialization
intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, help_command=None)

# Logging
logger = logging.getLogger("nextcord")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename="lene-nextcord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

logger.addHandler(handler)


## Events
# ON STARTUP:       Set activity and report online state when ready 
@bot.event
async def on_ready():
    print("\n\tLene#2184 is ready!")
    try:
        await bot.sync_application_commands()
        print("\tSynced global commands!")
    except Exception as e:
        print(e)
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="you <3"))


# ON SERVER JOIN:   Send greeting message & create server directory
@bot.event
async def on_guild_join(guild):
    print(f"Joined server {guild.id}!")
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Vielen Dank für die Einladung! <3")
        break
    os.mkdir(f"database\id_store\{guild.id}")


# ON SERVER LEAVE:  Clean up server directory
@bot.event
async def on_guild_remove(guild):
    print(f"Left server {guild.id}")
    shutil.rmtree(f"database\id_store\{guild.id}")



## Main run function
def main():
    # Load extensions
    print("Loading modules... \n")
    for folder in os.listdir("cogs"):
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            bot.load_extension(f"cogs.{folder}.cog")
    
    # Start the bot
    bot.run(token)

if __name__ == "__main__":
    main()
