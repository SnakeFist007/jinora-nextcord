import nextcord
import random
import requests
from nextcord import Interaction
from nextcord.ext import commands
from datetime import datetime
from main import logging
from main import qotd, QUOTES
from main import parse_json_utf8, raw_mystery, convert_raw, em_error


# Random, but same value for each day
def daily_random(length):
    seed = datetime.now() - datetime(2000, 4, 23)
    
    random.seed(seed.days)
    return random.randint(1, length)


# Initialize Cog
class QotD(commands.Cog, name="QotD"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # Questions
    @nextcord.slash_command(name="qotd", description="Question of the day!")
    async def qotd(self, interaction: Interaction):
        lines = parse_json_utf8(qotd)
        length = len(lines)

        rand_int = daily_random(length)
        output = lines[str(rand_int)]
        
        embed = {
            "title": f"{output}",
            "description": "Need something to reflect on? I've got you covered!\nCome back tomorrow for a new quote."
        }
        em = raw_mystery() | embed

        await interaction.response.send_message(embed=convert_raw(em), ephemeral=True)
       
    
    # Quotes
    @nextcord.slash_command(name="quote", description="Quote of the day!")
    async def quote(self, interaction: Interaction):
        url = "https://api.api-ninjas.com/v1/quotes?category=inspirational"
        res = requests.get(url, headers={"X-Api-Key": QUOTES})
        data = res.json()
        
        if res.status_code == requests.codes.ok:
            embed = {
                "title": f"{data[0]['quote']} *~{data[0]['author']}*",
                "description": "Sometimes quotes can be very insightful... Other times, not so much."
            }
            em = raw_mystery() | embed

            await interaction.response.send_message(embed=convert_raw(em), ephemeral=True)
        else:
            logging.exception("ERROR getting response from quotes API")
            await interaction.response.send_message(embed=em_error(), ephemeral=True)
            return


# Add Cog to bot
def setup(bot):
    bot.add_cog(QotD(bot))
    logging.info("QotD module loaded!")
