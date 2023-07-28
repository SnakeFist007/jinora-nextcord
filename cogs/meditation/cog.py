import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from main import logging

# Initialize Cog
class Meditation(commands.Cog, name="Meditation"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    # TODO: Add commands
    # Tips & videos on how to meditate
    # Beginner, Advanced, Expert levels
    # Global leaderboards?
    # Pomodoro
    # Add running timer


# Add Cog to bot
def setup(bot):
    bot.add_cog(Meditation(bot))
    logging.info("Meditation module loaded!")
