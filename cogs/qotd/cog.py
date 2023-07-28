import nextcord
import random
from nextcord import Interaction
from nextcord.ext import commands
from main import logging
from main import qotd
from main import parse_json_utf8, raw_mystery, convert_raw

# Initialize Cog
class QotD(commands.Cog, name="QotD"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # QotD
    # TODO: Seed that changes with time, so that you get the same question for every 24h
    # TODO: Daily posting into channel, at time X
    # TODO: Auto-Threading
    @nextcord.slash_command(name="qotd", description="Question of the day!")
    async def qotd(self, interaction: Interaction):
        lines = parse_json_utf8(qotd)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]
        
        embed = {
            "title": f"{output}"
        }
        em = raw_mystery() | embed

        await interaction.response.send_message(embed=convert_raw(em), ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(QotD(bot))
    logging.info("QotD module loaded!")
