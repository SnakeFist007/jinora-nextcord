import nextcord
import codecs
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
        # Replace before productive release: Huge workload, especially with bigger files...
        fortune_cookies = "database/db_fortune.txt"

        with codecs.open(fortune_cookies, "r", "utf-8") as f:
            lines = f.read().splitlines()
        ran = random.choice(lines)

        await interaction.response.send_message(f"{ran}", ephemeral=True)


    # @nextcord.slash_command(name="daily_fortune", description="Sagt dir die heutige Weisheit!", guild_ids=[testServerID])
    # async def daily_fortune(self, interaction: Interaction):
    #     await interaction.response.send_message("Work-in-Progress!", ephemeral=True)


    @nextcord.slash_command(name="8ball", description="Beantwortet dir eine Frage nach bestem Gewissen!", guild_ids=[testServerID])
    async def fortune_8ball(self, interaction: Interaction, frage: str = SlashOption(description="Stell deine Frage...")):
        # Replace before productive release: Huge workload, especially with bigger files...
        eight_ball = "database/db_8ball.txt" 

        with codecs.open(eight_ball, "r", "utf-8") as f:
            lines = f.read().splitlines()
        ran = random.choice(lines)

        await interaction.response.send_message(f"{ran}", ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Fortune(bot))
    print("Fortune module loaded!")
