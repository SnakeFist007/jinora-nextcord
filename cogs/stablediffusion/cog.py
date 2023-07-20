import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from .DrawButtons import DrawButtons

# Initialize Cog
class StableDiffusion(commands.Cog, name="StableDiffusion"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    # Generate
    @nextcord.slash_command(name="generate", description="Generiert ein Bild!")
    async def sd_generate(self, interaction: Interaction):
        view = DrawButtons()
        await interaction.response.send_message("Test!", view=view)
        await view.wait()
        
        if view.value == 1:
            await interaction.send_message("Auwahl: 1", ephemeral=True)
        elif view.value == 2:
            await interaction.send_message("Auwahl: 2", ephemeral=True)
        elif view.value == 3:
            await interaction.send_message("Auwahl: 3", ephemeral=True)
        else:
            return
        

# Add Cog to bot
def setup(bot):
    bot.add_cog(StableDiffusion(bot))
    print("Stable Diffusion module loaded!")
