import nextcord
import re
import random
import requests
import aiohttp
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands
from functions.helpers import JSONLoader, EmbedBuilder
from functions.logging import logging
from functions.paths import moon_phases
from main import QUOTES, WEATHER

def is_valid_time_format(input: str) -> bool:
    pattern = r"^\d{2}:\d{2}$"
    return bool(re.match(pattern, input))


# Initialize Cog
class Mood(commands.Cog, name="Mood"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Mood
    @nextcord.slash_command(name="mood", description="How's your mood?")
    async def main(self, interaction: Interaction) -> None:
        pass
    
    @commands.has_permissions(create_public_threads=True)
    @main.subcommand(name="poll", description="Ask the community!")
    async def mood_poll_manual(self, interaction: Interaction, 
                               role: nextcord.Role = SlashOption(description="Select a role to ping")) -> None:
        
        # Get a nice quote
        url = "https://api.api-ninjas.com/v1/quotes?category=inspirational"
        res = requests.get(url, headers={"X-Api-Key": QUOTES})
        data = res.json()

        if res.status_code == requests.codes.ok:
            quote = f"''{data[0]['quote']}'' *~{data[0]['author']}*"
        
        # Fallback to generic text, if API call fails
        else:
            logging.exception("ERROR getting response from quotes API")
            quote = "Let us know in the thread!"
        
        # Grab the current moon phase
        try:
            url = "https://api.weatherapi.com/v1/astronomy.json"
            params = { "key": WEATHER, "q": "Berlin" }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as res:
                    data = await res.json()

            moon_phase = data["astronomy"]["astro"]["moon_phase"]
            emoji_db = JSONLoader.load(moon_phases)
            moon = emoji_db[moon_phase.lower()]["emoji"]
        
        # Fallback to random (creepy) emote, if API call fails
        except KeyError as e:
            logging.exception(e)
            moon_phase = ["🌝", "🌚"]
            moon = random.choice(moon_phase)
        
        
        # Create embed
        embed = {
            "title": f"How happy were you today?",
            "description": quote
        }
        em = EmbedBuilder.bake_thumbnail(embed)

        # Send message & create thread
        await interaction.response.defer()
        message = await interaction.followup.send(embed=em)
        thread = await interaction.channel.create_thread(name=moon, message=message, type=ChannelType.public_thread)
        await thread.send(f"{role.mention}")
        
        
    # @commands.has_permissions(create_public_threads=True)
    # @main.subcommand(name="setup", description="Set up an automatic poll!")
    # async def mood_poll_auto(self, interaction: Interaction,
    #                          role: nextcord.Role = SlashOption(description="Select a role to ping"),
    #                          interval: int = SlashOption(description="Select an interval",
    #                                                      choices={
    #                                                          "Daily": 1,
    #                                                          "Weekly": 7
    #                                                      }),
    #                          time: str = SlashOption(description="Time in 24h 'HH:MM' format")) -> None:
    #     if is_valid_time_format(time):
    #         channel = interaction.channel
    #         msg = f"{role.mention} How are you doing today?"
            
            
    #         # Send message
    #         message = await interaction.send(msg)
    #         msg = await message.fetch()
    #         await interaction.channel.create_thread(name=f"☀️", message=msg, type=ChannelType.public_thread)
        

# Add Cog to bot
def setup(bot) -> None:
    bot.add_cog(Mood(bot))
    logging.info("Mood module loaded!")
