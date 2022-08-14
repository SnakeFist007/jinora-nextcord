import os
import env
import nextcord
from nextcord.ext import commands

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
