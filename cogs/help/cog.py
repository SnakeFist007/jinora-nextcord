import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from functions.helpers import EmbedBuilder
from functions.logging import logging
from functions.paths import SPARKLES, AIR_NOMAD, questioning
from cogs.help.ButtonView import HelpButtons


# Initialize Cog
class Help(commands.Cog, name="Help"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Help
    @nextcord.slash_command(name="help", description="Here to help!")
    async def help(self, interaction: Interaction) -> None:
        embed = {
            "title": f"{AIR_NOMAD}  Command Overview",
            "description": "Go through the pages for more detailed information!"
        }
        em = EmbedBuilder.bake_thumbnail(embed)
        
        em.add_field(
            name=f"{SPARKLES} `/feed ...`",
            value="Uses a webhook to generate a recurring reminder!\nIt will repeat at a set time on a given weekday.",
            inline=False
        )
        em.add_field(
            name=f"{SPARKLES} `/qotd` `/quote`",
            value="Inspirational questions, quotes and wisdoms for your spiritual journey!",
            inline=False
        )
        em.add_field(
            name=f"{SPARKLES} `/weather` `/astro`",
            value="Get the current weather or moon conditions for a given location!",
            inline=False
        )
        em.add_field(
            name=f"{SPARKLES} `/8ball` `/joke` `/wisdom`",
            value="Some fun commands to play around with!",
            inline=False
        )
        
        await interaction.response.send_message(file=EmbedBuilder.get_emoji(questioning), embed=em, view=HelpButtons())


# Add Cog to bot
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Help(bot))
    logging.info("Help module loaded!")
