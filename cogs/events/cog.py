import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from functions.logging import logging


# Initialize Cog
class Events(commands.Cog, name="Events"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Events
    @nextcord.slash_command(name="events", description="Not yet implemented!")
    async def events(self, interaction: Interaction) -> None:
        pass


# Add Cog to bot
def setup(bot) -> None:
    bot.add_cog(Events(bot))
    logging.info("Events module loaded!")
