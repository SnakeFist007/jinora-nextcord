import nextcord
import random
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from jokeapi import Jokes
from functions.helpers import JSONLoader, EmbedBuilder
from functions.logging import logging
from functions.paths import wisdom, eight_ball


JOKE_BLACKLIST = ["racist", "sexist", "nsfw"]

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

        await interaction.response.send_message(embed=EmbedBuilder.bake_questioning(embed), ephemeral=True)

    # Get an 8-Ball answer for a serious question
    @nextcord.slash_command(name="8ball", description="Answers important questions!")
    async def fortune_8ball(self, interaction: Interaction, question: str = SlashOption(description="Ask your question...")) -> None:
        lines = JSONLoader.load(eight_ball)
        length = len(lines)

        rand_int = random.randint(1, length)
        output = lines[str(rand_int)]
        
        embed = {
            "title": f"{output}",
            "description": "Asking the real questions here!"
        }

        await interaction.response.send_message(embed=EmbedBuilder.bake_questioning(embed), ephemeral=True)
        
    
    # Joke command
    @nextcord.slash_command(name="joke", description="Tells a joke!")
    async def joke(self, interaction: Interaction) -> None:
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
        
        await interaction.send(embed=EmbedBuilder.bake_joke(embed), ephemeral=True)


# Add Cog to bot
def setup(bot) -> None:
    bot.add_cog(Mystery(bot))
    logging.info("Mystery module loaded!")
