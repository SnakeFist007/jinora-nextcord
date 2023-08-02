import nextcord
import aiohttp
from nextcord.interactions import Interaction
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from functions.helpers import parse_json, bake_embed_thumbnail, em_error
from functions.logging import logging
from functions.paths import conditions, moon_phases
from main import WEATHER


# Initialize Cog
class Weather(commands.Cog, name="Weather"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    # Weather command
    @nextcord.slash_command(name="weather", description="Generates a weather report!")
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
            emoji_db = parse_json(conditions)
            emoji = emoji_db[condition.lower()]["emoji"]
            thumbnail = emoji_db[condition.lower()]["thumbnail"]
        except KeyError as e:
            logging.exception(e)
            await interaction.send(embed=em_error(), ephemeral=True)
            return
                
        embed = {
            "title": f"{emoji} Jinora's Weather Report Service", 
            "description": f"My sources say that the current condition in {city} is {condition.lower()}!"
        }
        em = bake_embed_thumbnail(embed)
                
        em.add_field(name="Temperature", value=f"{data['current']['temp_c']}°C")
        em.add_field(name="Humidity", value=f"{data['current']['humidity']}%")
        em.add_field(name="Wind Speeds", value=f"{int(data['current']['wind_kph'])} km/h")
        
        em.set_thumbnail(url=thumbnail)
                
        await interaction.send(embed=em, ephemeral=True)
        
        
    # Astro command
    @nextcord.slash_command(name="astro", description="Generates an astro report!")
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
            emoji_db = parse_json(moon_phases)
            emoji = emoji_db[moon_phase.lower()]["emoji"]
            thumbnail = emoji_db[moon_phase.lower()]["thumbnail"]
        except KeyError as e:
            logging.exception(e)
            await interaction.send(embed=em_error(), ephemeral=True)
            return
                
        embed = {
            "title": f"{emoji} Jinora's Astro Report Service", 
            "description": f"The current moon phase in {city} is {moon_phase.lower()}!"
        }
        em = bake_embed_thumbnail(embed)
                
        em.add_field(name="Moonrise", value=f"{data['astronomy']['astro']['moonrise']}")
        em.add_field(name="Moonset", value=f"{data['astronomy']['astro']['moonset']}")
        em.add_field(name="Moon Illumination", value=f"{data['astronomy']['astro']['moon_illumination']}%")
        
        em.set_thumbnail(url=thumbnail)
                
        await interaction.send(embed=em, ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Weather(bot))
    logging.info("Weather functions loaded!")
