import nextcord
import json
import random
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from main import logging, parse_json_utf8

# Initialize Cog
class Mystery(commands.Cog, name="Mystery"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Get a fortune
    @nextcord.slash_command(name="fortune", description="Tells a random fortune!")
    async def fortune_cookie(self, interaction: Interaction):
        fortune_cookies = "database/db_fortune.json"
        
        with open(fortune_cookies, encoding="utf-8") as f:
            lines = json.load(f)
            
        lines = parse_json_utf8(fortune_cookies)
        length = len(lines[0])
        
        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]

        await interaction.response.send_message(f"{output}", ephemeral=True)


    # Get an 8-Ball answer for a serious question
    @nextcord.slash_command(name="8ball", description="Answers important questions!")
    async def fortune_8ball(self, interaction: Interaction, frage: str = SlashOption(description="Ask your question...")):
        eight_ball_answers = "database/db_8ball.json"
        
        lines = parse_json_utf8(eight_ball_answers)
        length = len(lines[0])
            
        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]

        await interaction.response.send_message(f"{output}", ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Mystery(bot))
    logging.info("Mystery module loaded!")
