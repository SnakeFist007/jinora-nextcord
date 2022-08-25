import nextcord
import json
import random
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from main import testServerID

# Initialize Cog
class Fortune(commands.Cog, name="Fortune"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="fortune", description="Sagt dir eine zufällige Weisheit!", guild_ids=[testServerID])
    async def fortune_cookie(self, interaction: Interaction):
        fortune_cookies = "database/db_fortune.json"
        
        with open(fortune_cookies, encoding="utf-8") as f:
            lines = json.load(f)
        
        length = len(lines[0])
        
        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]

        await interaction.response.send_message(f"{output}", ephemeral=True)


    @nextcord.slash_command(name="8ball", description="Beantwortet dir eine Frage nach bestem Gewissen!", guild_ids=[testServerID])
    async def fortune_8ball(self, interaction: Interaction, frage: str = SlashOption(description="Stell deine Frage...")):
        eight_ball_answers = "database/db_8ball.json"
        
        with open(eight_ball_answers, encoding="utf-8") as f:
            lines = json.load(f)
            
        length = len(lines[0])
            
        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]

        await interaction.response.send_message(f"{output}", ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Fortune(bot))
    print("Fortune module loaded!")
