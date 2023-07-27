import nextcord
import random
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from main import logging
from main import parse_json_utf8, bake_embed


# Initialize Cog
class Mystery(commands.Cog, name="Mystery"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # TODO: Give the wisdoms a Jinora personality, remove old cookie messages
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

    # TODO: Give the 8-Ball answers a Jinora personality
    # Get an 8-Ball answer for a serious question
    @nextcord.slash_command(name="8ball", description="Answers important questions!")
    async def fortune_8ball(self, interaction: Interaction, question: str = SlashOption(description="Ask your question...")):
        eight_ball_answers = "database/db_8ball.json"

        lines = parse_json_utf8(eight_ball_answers)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]
        
        embed = {
            "title": f"{output}",
            "description": "Asking the real questions here!"
        }

        await interaction.response.send_message(embed=bake_embed(embed), ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Mystery(bot))
    logging.info("Mystery module loaded!")
