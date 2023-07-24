import nextcord
import json
import random
from nextcord import Interaction, SlashOption, Embed
from nextcord.ext import commands
from main import logging, parse_json_utf8, parse_json

# Initialize Cog
class Mystery(commands.Cog, name="Mystery"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Get a fortune
    @nextcord.slash_command(name="fortune", description="Tells a random fortune!")
    async def fortune_cookie(self, interaction: Interaction):
        fortune_cookies = "database/db_fortune.json"

        lines = parse_json_utf8(fortune_cookies)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]

        embed1 = parse_json("database/embeds/standard_embed.json")
        embed2 = {
            "title": "Fortune Cookie",
            "description": f"{output}"
        }
        em = Embed().from_dict(embed1 | embed2)

        await interaction.response.send_message(embed=em, ephemeral=True)

    # Get an 8-Ball answer for a serious question
    @nextcord.slash_command(name="8ball", description="Answers important questions!")
    async def fortune_8ball(self, interaction: Interaction, frage: str = SlashOption(description="Ask your question...")):
        eight_ball_answers = "database/db_8ball.json"

        lines = parse_json_utf8(eight_ball_answers)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]
        
        embed1 = parse_json("database/embeds/standard_embed.json")
        embed2 = {
            "title": "8-Ball Answer",
            "description": f"{output}"
        }
        em = Embed().from_dict(embed1 | embed2)

        await interaction.response.send_message(embed=em, ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Mystery(bot))
    logging.info("Mystery module loaded!")
