import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands
from functions.logging import logging


# Initialize Cog
class Mood(commands.Cog, name="Mood"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Mood
    @commands.has_permissions(create_public_threads=True)
    @nextcord.slash_command(name="mood", description="Not yet implemented!")
    async def mood_reminder(self, interaction: Interaction, 
                            role: nextcord.Role = SlashOption(description="Select a role to ping")) -> None:
        
        message = await interaction.send(f"{role.mention} How are you doing today?")
        msg = await message.fetch()
        await interaction.channel.create_thread(name=f"☀️", message=msg, type=ChannelType.public_thread)
        

# Add Cog to bot
def setup(bot) -> None:
    bot.add_cog(Mood(bot))
    logging.info("Mood module loaded!")
