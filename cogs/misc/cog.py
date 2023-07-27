import nextcord
import aiohttp
from nextcord.interactions import Interaction
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from jokeapi import Jokes
from main import logging
from main import db_servers
from main import parse_json, bake_embed, bake_embed_thumbnail, em_error
from main import WEATHER


CONDITIONS = "database/weather_conditions.json"

# Initialize Cog
class Basics(commands.Cog, name="Misc"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

    # General stats of the bot
    @nextcord.slash_command(name="status", description="Pong!")
    async def status(self, interaction: Interaction):
        logging.info("Checking status...")
        # Get amount of servers joined
        count = db_servers.joined_servers_list.count_documents({})
        # Calculate latency
        ping = round(self.bot.latency * 1000)
        logging.info(f"Ping is {ping}ms.")

        embed = {
            "description": f"Amount of Servers joined: `{count}`\nPing: `{ping}ms`"
        }

        await interaction.send(embed=bake_embed(embed), ephemeral=True)
        
    # Weather command
    @nextcord.slash_command(name="weather", description="Tells the weather!")
    async def weather(self, interaction: Interaction, location: str = SlashOption()):
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": WEATHER,
            "q": location
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as res:
                    data = await res.json()
                    
            city = data["location"]["name"]
            condition = data["current"]["condition"]["text"]
            emoji_db = parse_json(CONDITIONS)
            emoji = emoji_db[condition.lower()]["emoji"]
            thumbnail = emoji_db[condition.lower()]["thumbnail"]
        except KeyError:
            await interaction.send(embed=em_error())
            return
                
        embed = {
            "title": f"{emoji} Weather report for: {city}", 
            "description": f"My sources say that the current condition in {city} is {condition.lower()}!"
        }
        em = bake_embed_thumbnail(embed)
                
        em.add_field(name="Temperature", value=f"{data['current']['temp_c']}° C")
        em.add_field(name="Humidity", value=f"{data['current']['humidity']}%")
        em.add_field(name="Wind Speeds", value=f"{int(data['current']['wind_kph'])} km/h")
        
        # TODO: Add different Jinora thumbnails for weather conditions
        # em.set_thumbnail(url=thumbnail)
                
        await interaction.send(embed=em, ephemeral=True)


    @nextcord.slash_command(name="joke", description="Tells a joke!")
    async def joke(self, interaction: Interaction):
        j = await Jokes()
        blacklist = ["racist", "sexist", "nsfw"]
        joke = await j.get_joke(blacklist=blacklist)
        
        if joke["type"] == "single":
            embed = {
                "title": joke["joke"] 
            }
        else:
            embed = {
                "title": joke['setup'],
                "description": f"||{joke['delivery']}||"
            }         
        
        await interaction.send(embed=bake_embed(embed), ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Basics(bot))
    logging.info("Basic functions loaded!")
