import nextcord
import random
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from main import logging
from main import parse_json_utf8, raw_mystery, convert_raw

WISDOM = "database/mystery/db_wisdom.json"
EIGHT_BALL = "database/mystery/db_8ball.json"

# Initialize Cog
class Mystery(commands.Cog, name="Mystery"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Get a random wisdom
    @nextcord.slash_command(name="wisdom", description="Tells a random wisdom!")
    async def wisdom(self, interaction: Interaction):
        lines = parse_json_utf8(WISDOM)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]

        embed = {
            "title": "Random Wisdom",
            "description": f"{output}"
        }
        em = raw_mystery() | embed

        await interaction.response.send_message(embed=convert_raw(em), ephemeral=True)

    # Get an 8-Ball answer for a serious question
    @nextcord.slash_command(name="8ball", description="Answers important questions!")
    async def fortune_8ball(self, interaction: Interaction, question: str = SlashOption(description="Ask your question...")):
        lines = parse_json_utf8(EIGHT_BALL)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]
        
        embed = {
            "title": f"{output}",
            "description": "Asking the real questions here!"
        }
        em = raw_mystery() | embed

        await interaction.response.send_message(embed=convert_raw(em), ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Mystery(bot))
    logging.info("Mystery module loaded!")
