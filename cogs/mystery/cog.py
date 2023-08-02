import nextcord
import random
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from jokeapi import Jokes
from functions.helpers import parse_json_utf8, raw_mystery, convert_raw, raw_joke
from functions.logging import logging
from functions.paths import wisdom, eight_ball


JOKE_BLACKLIST = ["racist", "sexist", "nsfw"]

# Initialize Cog
class Mystery(commands.Cog, name="Mystery"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Get a random wisdom
    @nextcord.slash_command(name="wisdom", description="Tells a random wisdom!")
    async def wisdom(self, interaction: Interaction):
        lines = parse_json_utf8(wisdom)
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
        lines = parse_json_utf8(eight_ball)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]
        
        embed = {
            "title": f"{output}",
            "description": "Asking the real questions here!"
        }
        em = raw_mystery() | embed

        await interaction.response.send_message(embed=convert_raw(em), ephemeral=True)
        
    
    # Joke command
    @nextcord.slash_command(name="joke", description="Tells a joke!")
    async def joke(self, interaction: Interaction):
        j = await Jokes()
        joke = await j.get_joke(blacklist=JOKE_BLACKLIST)
        
        if joke["type"] == "single":
            embed = {
                "title": joke["joke"] 
            }
        else:
            embed = {
                "title": joke['setup'],
                "description": f"||{joke['delivery']}||"
            }
        em = raw_joke() | embed
        
        await interaction.send(embed=convert_raw(em), ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Mystery(bot))
    logging.info("Mystery module loaded!")
