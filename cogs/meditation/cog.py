import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from functions.logging import logging


# Initialize Cog
class Meditation(commands.Cog, name="Meditation"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Meditation
    @nextcord.slash_command(name="meditation", description="Not yet implemented!")
    async def main(self, interaction: Interaction):
        pass
    
    
    @main.subcommand(name="tips", description="Not yet implemented!")
    async def meditation_tips(self, interaction: Interaction):
        pass


    @main.subcommand(name="weekly", description="Not yet implemented!")
    async def meditation_weekly(self, interaction: Interaction):
        pass



# Add Cog to bot
def setup(bot):
    bot.add_cog(Meditation(bot))
    logging.info("Meditation module loaded!")
