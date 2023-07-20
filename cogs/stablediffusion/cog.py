import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

# Initialize Cog
class StableDiffusion(commands.Cog, name="StableDiffusion"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

# Add Cog to bot
def setup(bot):
    bot.add_cog(StableDiffusion(bot))
    print("StableDiffusion module loaded!")
