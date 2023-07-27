import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from main import logging
from main import em_help

# Initialize Cog
class Help(commands.Cog, name="Help"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Help
    @nextcord.slash_command(name="help", description="Here to help!")
    async def help(self, interaction: Interaction):
        await interaction.response.send_message(embed=em_help(), ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Help(bot))
    logging.info("Help module loaded!")
