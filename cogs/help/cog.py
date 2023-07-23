import nextcord
from nextcord import Interaction
from nextcord.ext import commands

# Initialize Cog
class Help(commands.Cog, name="Help"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    # Help
    @nextcord.slash_command(name="help", description="Here to help!")
    async def help(self, interaction: Interaction):
        em = nextcord.Embed(
            title="Liste der Befehle",
            description="""
            `/generate` - creates an image using Stable Diffusion
            `/status` - displays Bot and Stable Diffusion status
            `/remindme` - creates a reminder
            `/8ball` - answers all your questions...
            `/fortune` - tells you a random fortune!""",
            colour=0x00b0f4)

        em.set_footer(text="Lene#2184", icon_url="https://i.imgur.com/k9t5gF7.png")

        await interaction.response.send_message(embed=em)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Help(bot))
    print("Help module loaded!")
