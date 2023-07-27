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
MOON_PHASES = "database/moon_phases.json"

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
        try:
            url = "https://api.weatherapi.com/v1/current.json"
            params = {
                "key": WEATHER,
                "q": location
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as res:
                    data = await res.json()
                    
            city = data["location"]["name"]
            condition = data["current"]["condition"]["text"]
            emoji_db = parse_json(CONDITIONS)
            emoji = emoji_db[condition.lower()]["emoji"]
            thumbnail = emoji_db[condition.lower()]["thumbnail"]
        except KeyError as e:
            logging.exception(e)
            await interaction.send(embed=em_error(), ephemeral=True)
            return
                
        embed = {
            "title": f"{emoji} Weather report for: {city}", 
            "description": f"My sources say that the current condition in {city} is {condition.lower()}!"
        }
        em = bake_embed_thumbnail(embed)
                
        em.add_field(name="Temperature", value=f"{data['current']['temp_c']}° C")
        em.add_field(name="Humidity", value=f"{data['current']['humidity']}%")
        em.add_field(name="Wind Speeds", value=f"{int(data['current']['wind_kph'])} km/h")
        
        em.set_thumbnail(url=thumbnail)
                
        await interaction.send(embed=em, ephemeral=True)
        
        
    # Astro command
    @nextcord.slash_command(name="astro", description="Tells the moon phase!")
    async def astro(self, interaction: Interaction, location: str = SlashOption()):
        try:
            url = "https://api.weatherapi.com/v1/astronomy.json"
            params = {
                "key": WEATHER,
                "q": location
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as res:
                    data = await res.json()
                    
            city = data["location"]["name"]
            moon_phase = data["astronomy"]["astro"]["moon_phase"]
            emoji_db = parse_json(MOON_PHASES)
            emoji = emoji_db[moon_phase.lower()]["emoji"]
            thumbnail = emoji_db[moon_phase.lower()]["thumbnail"]
        except KeyError as e:
            logging.exception(e)
            await interaction.send(embed=em_error(), ephemeral=True)
            return
                
        embed = {
            "title": f"{emoji} Astro report for: {city}", 
            "description": f"The current moon phase in {city} is {moon_phase.lower()}!"
        }
        em = bake_embed_thumbnail(embed)
                
        em.add_field(name="Moonrise", value=f"{data['astronomy']['astro']['moonrise']}")
        em.add_field(name="Moonset", value=f"{data['astronomy']['astro']['moonset']}")
        em.add_field(name="Moon Illumination", value=f"{data['astronomy']['astro']['moon_illumination']}%")
        
        em.set_thumbnail(url=thumbnail)
                
        await interaction.send(embed=em, ephemeral=True)


    # Joke command
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
