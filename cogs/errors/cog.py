import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from functions.logging import logging


# Initialize Cog
class Errors(commands.Cog, name="Errors"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Listener


# Add Cog to bot
def setup(bot):
    bot.add_cog(Errors(bot))
    logging.info("Error module loaded!")
