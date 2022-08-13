import os
import env
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

# Variables
token_file = open("token.auth", "r")
token = token_file.read()

### DEBUG - REMOVE BEFORE PRODUCTIVE RELEASE!!!
testServerID = env.server_id

# Intents & Bot initialization
intents = nextcord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

# Events
@bot.event
async def on_ready():
    print("\n\tLene#2184 is ready!")
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="you <3"))


# Load cogs
@bot.slash_command(name="load", description="Loads a cog", guild_ids=[testServerID])
@commands.is_owner()
async def load_cog(interaction: Interaction, cog: str = SlashOption(description="Choose the cog")):
    print(f"Loading {cog} module...")
    bot.load_extension(f"cogs.{cog}.cog")
    await interaction.response.send_message(f"Loaded cog **{cog}**!", ephemeral=True)

# Reload cogs
@bot.slash_command(name="reload", description="Reloads a cog", guild_ids=[testServerID])
@commands.is_owner()
async def reload_cog(interaction: Interaction, cog: str = SlashOption(description="Choose the cog")):
    print(f"Reloading {cog} module...")
    bot.reload_extension(f"cogs.{cog}.cog")
    await interaction.response.send_message(f"Reloaded cog **{cog}**!", ephemeral=True)

# Unload cogs
@bot.slash_command(name="unload", description="Unloads a cog", guild_ids=[testServerID])
@commands.is_owner()
async def unload_cog(interaction: Interaction, cog: str = SlashOption(description="Choose the cog")):
    print(f"Unloading {cog} module...")
    bot.unload_extension(f"cogs.{cog}.cog")
    print(f"Unloaded {cog} module!")
    await interaction.response.send_message(f"Unloaded cog **{cog}**!", ephemeral=True)


# Shutdown bot
@bot.slash_command(name="logout", description="[!!!] Shuts down the bot [!!!]", guild_ids=[testServerID])
@commands.is_owner()
async def bot_shutdown(interaction: Interaction):
    await interaction.response.send_message("**SHUTTING DOWN THE BOT**", ephemeral=True)
    await bot.close()


def main():
    # Load extensions
    for folder in os.listdir("cogs"):
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            bot.load_extension(f"cogs.{folder}.cog")
    
    # Start the bot
    bot.run(token)

if __name__ == "__main__":
    main()
