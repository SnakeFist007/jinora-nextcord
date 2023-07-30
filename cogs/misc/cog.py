import nextcord
from nextcord.interactions import Interaction
from nextcord import Interaction
from nextcord.ext import commands
from main import logging
from main import db_servers
from main import bake_embed
from main import VERSION


# Initialize Cog
class Basics(commands.Cog, name="Misc"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

    # General stats of the bot
    @nextcord.slash_command(name="status", description="Bot status and statistics!")
    async def status(self, interaction: Interaction):
        logging.info("Checking status...")
        # Get amount of servers joined
        count = db_servers.joined_servers_list.count_documents({})
        # Calculate latency
        ping = round(self.bot.latency * 1000)
        logging.info(f"Ping is {ping}ms.")

        embed = {
            "title": "Status Page",
            "description": f"Version: `{VERSION}`\nPing: `{ping}ms`\nAmount of Servers joined: `{count}`"
        }

        await interaction.send(embed=bake_embed(embed), ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Basics(bot))
    logging.info("Basic functions loaded!")
