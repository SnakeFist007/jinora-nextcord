import nextcord
import re
import random
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands, application_checks
from functions.apis import get_quote, get_astro
from functions.helpers import JSONLoader, EmbedBuilder
from functions.logging import logging
from functions.paths import moon_phases
from functions.errors import default_error, dm_error


def is_valid_time_format(input: str) -> bool:
    pattern = r"^\d{2}:\d{2}$"
    return bool(re.match(pattern, input))


# Initialize Cog
class Mood(commands.Cog, name="Mood"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Mood
    @nextcord.slash_command(name="mood", description="How's your mood?")
    @application_checks.guild_only()
    @application_checks.has_permissions(manage_messages=True)
    async def main(self, interaction: Interaction) -> None:
        pass
    
    
    @main.subcommand(name="poll", description="Ask the community!")
    @application_checks.guild_only()
    @application_checks.has_permissions(manage_messages=True)
    @commands.has_permissions(create_public_threads=True)
    async def mood_poll_manual(self, interaction: Interaction, 
                               role: nextcord.Role = SlashOption(description="Select a role to ping")) -> None:
        
        # Get a nice quote
        try:
            data = await get_quote()
            quote = f"''{data[0]['quote']}'' *~{data[0]['author']}*"        
        # Fallback to generic text, if API call fails
        except ValueError:
            logging.exception("ERROR getting response from quotes API")
            quote = "Let us know in the thread!"
        
        # Grab the current moon phase
        try:
            data = await get_astro("Berlin")

            moon_phase = data["astronomy"]["astro"]["moon_phase"]
            emoji_db = JSONLoader.load(moon_phases)
            moon = emoji_db[moon_phase.lower()]["emoji"]
        # Fallback to random (creepy) emote, if API call fails
        except ValueError:
            logging.exception("ERROR getting response from quotes API")
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
        
    @mood_poll_manual.error
    async def on_command_error(self, interaction: Interaction, error) -> None:
        if isinstance(error, application_checks.errors.ApplicationNoPrivateMessage):
            await dm_error(interaction)
        else:
            await default_error(interaction)
            
# Add Cog to bot
def setup(bot) -> None:
    bot.add_cog(Mood(bot))
    logging.info("Mood module loaded!")
