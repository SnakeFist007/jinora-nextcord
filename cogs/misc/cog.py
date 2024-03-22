import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from functions.helpers import EmbedBuilder
from functions.logging import logging
from functions.paths import SPARKLES, AIR_NOMAD, sunny
from main import db_servers, VERSION


# Initialize Cog
class Basics(commands.Cog, name="Misc"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        

    # General stats of the bot
    @nextcord.slash_command(name="status", description="Bot status and statistics!")
    async def status(self, interaction: Interaction) -> None:
        logging.info("Checking status...")
        # Get amount of servers joined
        count = db_servers.joined_servers_list.count_documents({})
        # Calculate latency
        ping = round(self.bot.latency * 1000)
        logging.info(f"Ping is {ping}ms.")

        embed = {
            "title": f"{AIR_NOMAD}  Status Page",
        }
        em = EmbedBuilder.bake(embed)
        
        em.add_field(
            name=f"{SPARKLES} Version:",
            value=f"`v{VERSION}`"
        )
        em.add_field(
            name=f"{SPARKLES} # of Servers joined:",
            value=f"`{count} Servers`"
        )
        em.add_field(
            name=f"{SPARKLES} Ping:",
            value=f"`{ping}ms`"
        )

        await interaction.send(file=EmbedBuilder.get_emoji(sunny), embed=em, ephemeral=True)


# Add Cog to bot
def setup(bot: commands.Bot):
    bot.add_cog(Basics(bot))
    logging.info("Basic functions loaded!")
