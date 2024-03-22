import nextcord
import random
from nextcord import Interaction
from nextcord.ext import commands
from functions.helpers import JSONLoader, EmbedBuilder
from functions.logging import logging
from functions.paths import wisdom, laughing


# Initialize Cog
class Mystery(commands.Cog, name="Mystery"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Get a random wisdom
    @nextcord.slash_command(name="wisdom", description="Tells a random wisdom!")
    async def wisdom(self, interaction: Interaction) -> None:
        lines = JSONLoader.load(wisdom)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]

        embed = {
            "title": "Random Wisdom",
            "description": f"{output}"
        }

        await interaction.response.send_message(file=EmbedBuilder.get_emoji(laughing), embed=EmbedBuilder.bake_thumbnail(embed), ephemeral=True)


# Add Cog to bot
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Mystery(bot))
    logging.info("Mystery module loaded!")
