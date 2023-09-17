import nextcord
import random
from nextcord import Interaction
from nextcord.ext import commands, application_checks
from datetime import datetime
from functions.apis import get_quote
from functions.errors import default_error, dm_error
from functions.helpers import EmbedBuilder, JSONLoader
from functions.logging import logging
from functions.paths import qotd


# Random, but same value for each day
def daily_random(length: int) -> int:
    seed = datetime.now() - datetime(2000, 4, 23)
    
    random.seed(seed.days)
    return random.randint(1, length)


# Initialize Cog
class QotD(commands.Cog, name="QotD"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    # Questions
    @nextcord.slash_command(name="question", description="Question of the day!")
    @application_checks.guild_only()
    async def question(self, interaction: Interaction) -> None:
        lines = JSONLoader.load(qotd)
        length = len(lines)

        rand_int = daily_random(length)
        output = lines[str(rand_int)]
        
        embed = {
            "title": f"{output}",
            "description": "Need something to reflect on? I've got you covered!\nCome back tomorrow for a new quote."
        }

        await interaction.response.send_message(embed=EmbedBuilder.bake_questioning(embed))
    
    
    # Quotes
    @nextcord.slash_command(name="quote", description="Quote of the day!")
    @application_checks.guild_only()
    async def quote(self, interaction: Interaction) -> None:
        try: 
            data = await get_quote()
            embed = {
                "title": f"{data[0]['quote']} *~{data[0]['author']}*",
                "description": "Sometimes quotes can be very insightful... Other times, not so much."
            }
        
            await interaction.response.send_message(embed=EmbedBuilder.bake(embed))
            
        except ValueError:
            logging.exception("ERROR getting response from quotes API")
            raise commands.errors.BadArgument

    @quote.error
    @question.error
    async def on_command_error(self, interaction: Interaction, error) -> None:
        if isinstance(error, commands.errors.BadArgument):
            await default_error(interaction)
        if isinstance(error, application_checks.errors.ApplicationNoPrivateMessage):
            await dm_error(interaction)
        else:
            await default_error(interaction)
        

# Add Cog to bot
def setup(bot) -> None:
    bot.add_cog(QotD(bot))
    logging.info("QotD module loaded!")
