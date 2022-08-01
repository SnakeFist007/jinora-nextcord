import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from main import testServerID

# Initialize Cog
class Basics(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="ping", description="Pong!", guild_ids=[testServerID])
    async def ping(self, interaction: Interaction):
        await interaction.send(f"Pong! (`Latency: {round(self.bot.latency * 1000)}ms`)")

# Add Cog to bot
def setup(bot):
    bot.add_cog(Basics(bot))
    print ("Basic functions loaded!")