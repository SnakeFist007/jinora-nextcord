import os
import env
import nextcord
from nextcord.ext import commands

# TODO: Add proper logging (save to file / crash-dumps)

# Variables
token_file = open("token.auth", "r")
token = token_file.read()

### DEBUG - REMOVE BEFORE PRODUCTIVE RELEASE!!!
testServerID = env.server_id

# Intents & Bot initialization
intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents)

# Events
@bot.event
async def on_ready():
    print("\n\tLene#2184 is ready!")
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="you <3"))

# Send greeting message & create server directory
@bot.event
async def on_guild_join(guild):
    print(f"Joined server {guild.id}!")
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Test message!")
        break
    # TODO: Add separate server storage (for characters)

# Clean up server directory  
@bot.event
async def on_guild_remove(guild):
    print(f"Left server {guild.id}")
    # TODO: Remove separate server storage (for characters)


# Main run function
def main():
    # Load extensions
    for folder in os.listdir("cogs"):
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            bot.load_extension(f"cogs.{folder}.cog")
    
    # Start the bot
    bot.run(token)

if __name__ == "__main__":
    main()
