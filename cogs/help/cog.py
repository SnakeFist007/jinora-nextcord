import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from functions.helpers import EmbedBuilder
from functions.logging import logging
from cogs.help.ButtonView import HelpButtons


# Initialize Cog
class Help(commands.Cog, name="Help"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Help
    @nextcord.slash_command(name="help", description="Here to help!")
    async def help(self, interaction: Interaction):
        embed = {
            "title": "⚙️ Command Overview",
            "description": "Go through the pages for more detailed information!"
        }
        em = EmbedBuilder.bake_questioning(embed)
        
        em.add_field(
            name="✨ `/feed ...`",
            value="Uses a webhook to generate a recurring reminder!\nIt will repeat at a set time on a given weekday.",
            inline=False
        )
        em.add_field(
            name="✨ `/qotd` `/quote`",
            value="Inspirational questions, quotes and wisdoms for your spiritual journey!",
            inline=False
        )
        em.add_field(
            name="✨ `/weather` `/astro`",
            value="Get the current weather or moon conditions for a given location!",
            inline=False
        )
        em.add_field(
            name="✨ `/8ball` `/joke` `/wisdom`",
            value="Some fun commands to play around with!",
            inline=False
        )
        
        await interaction.response.send_message(embed=em, view=HelpButtons(), ephemeral=True)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Help(bot))
    logging.info("Help module loaded!")
