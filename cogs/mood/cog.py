import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from functions.logging import logging


# Initialize Cog
class Mood(commands.Cog, name="Mood"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Mood
    @nextcord.slash_command(name="mood", description="Not yet implemented!")
    async def main(self, interaction: Interaction) -> None:
        pass
    
    
    @main.subcommand(name="log", description="Not yet implemented!")
    async def meditation_tips(self, interaction: Interaction) -> None:
        pass


    @main.subcommand(name="reminder", description="Not yet implemented!")
    async def meditation_weekly(self, interaction: Interaction) -> None:
        pass



# Add Cog to bot
def setup(bot) -> None:
    bot.add_cog(Mood(bot))
    logging.info("Meditation module loaded!")
