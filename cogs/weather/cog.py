import nextcord
from nextcord.interactions import Interaction
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from functions.apis import get_weather, get_astro
from functions.errors import default_error
from functions.helpers import JSONLoader, EmbedBuilder
from functions.logging import logging
from functions.paths import conditions, moon_phases, emotes


# Initialize Cog
class Weather(commands.Cog, name="Weather"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    # Weather command
    @nextcord.slash_command(name="weather", description="Generates a weather report!")
    async def weather(self, interaction: Interaction, location: str = SlashOption()) -> None:
        try:
            data = await get_weather(location)
                    
            city = data["location"]["name"]
            condition = data["current"]["condition"]["text"]
            emoji_db = JSONLoader.load(conditions)
            emoji = emoji_db[condition.lower()]["emoji"]
            thumbnail = emotes[f"{emoji_db[condition.lower()]['thumbnail']}"]
            
        except KeyError as e:
            logging.exception(e)
            raise commands.errors.BadArgument
                
        embed = {
            "title": f"{emoji} Jinora's Weather Report Service", 
            "description": f"My sources say that the current condition in {city} is {condition.lower()}!"
        }
        em = EmbedBuilder.bake_thumbnail(embed)
                
        em.add_field(name="Temperature", value=f"{data['current']['temp_c']}°C")
        em.add_field(name="Humidity", value=f"{data['current']['humidity']}%")
        em.add_field(name="Wind Speeds", value=f"{int(data['current']['wind_kph'])} km/h")
                
        await interaction.send(file=EmbedBuilder.get_emoji(thumbnail), embed=em)
        
        
    # Astro command
    @nextcord.slash_command(name="astro", description="Generates an astro report!")
    async def astro(self, interaction: Interaction, location: str = SlashOption()) -> None:
        try:
            data = await get_astro(location)
                    
            city = data["location"]["name"]
            moon_phase = data["astronomy"]["astro"]["moon_phase"]
            emoji_db = JSONLoader.load(moon_phases)
            emoji = emoji_db[moon_phase.lower()]["emoji"]
            thumbnail = emotes[f"{emoji_db[moon_phase.lower()]['thumbnail']}"]
            
        except KeyError as e:
            logging.exception(e)
            raise commands.errors.BadArgument
                
        embed = {
            "title": f"{emoji} Jinora's Astro Report Service", 
            "description": f"The current moon phase in {city} is {moon_phase.lower()}!"
        }
        em = EmbedBuilder.bake_thumbnail(embed)
                
        em.add_field(name="Moonrise", value=f"{data['astronomy']['astro']['moonrise']}")
        em.add_field(name="Moonset", value=f"{data['astronomy']['astro']['moonset']}")
        em.add_field(name="Moon Illumination", value=f"{data['astronomy']['astro']['moon_illumination']}%")
                
        await interaction.send(file=EmbedBuilder.get_emoji(thumbnail), embed=em)

    @weather.error
    @astro.error
    async def on_command_error(self, interaction: Interaction, error) -> None:
        await default_error(interaction)


# Add Cog to bot
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Weather(bot))
    logging.info("Weather functions loaded!")
