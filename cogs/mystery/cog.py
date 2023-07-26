import nextcord
import random
from nextcord import Interaction, SlashOption, Embed
from nextcord.ext import commands
from main import logging, parse_json_utf8, bake_embed

# Initialize Cog
class Mystery(commands.Cog, name="Mystery"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Get a random wisdom
    @nextcord.slash_command(name="wisdom", description="Tells a random wisdom!")
    async def wisdom(self, interaction: Interaction):
        wisdom = "database/db_wisdom.json"

        lines = parse_json_utf8(wisdom)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]

        embed = {
            "title": "Random Wisdom",
            "description": f"{output}"
        }

        await interaction.response.send_message(embed=bake_embed(embed), ephemeral=True)

    # Get an 8-Ball answer for a serious question
    @nextcord.slash_command(name="8ball", description="Answers important questions!")
    async def fortune_8ball(self, interaction: Interaction, frage: str = SlashOption(description="Ask your question...")):
        eight_ball_answers = "database/db_8ball.json"

        lines = parse_json_utf8(eight_ball_answers)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]
        
        embed = {
            "title": "8-Ball Answer",
            "description": f"{output}"
        }

        await interaction.response.send_message(embed=bake_embed(embed), ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Mystery(bot))
    logging.info("Mystery module loaded!")
