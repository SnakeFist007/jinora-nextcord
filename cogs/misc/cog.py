import nextcord
import asyncio
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from typing import Optional
from main import testServerID

# Initialize Cog
class Basics(commands.Cog, name="Misc"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Debug / Test-Command to see how well the bot is doing
    @nextcord.slash_command(name="ping", description="Pong!", guild_ids=[testServerID])
    async def ping(self, interaction: Interaction):
        await interaction.send(f"Pong! (`Latency: {round(self.bot.latency * 1000)}ms`)")
    
    # Reminder command (Supported: seconds, months, hours & days)
    @nextcord.slash_command(name="remindme", description="Lass dich an Dinge erinnern!", guild_ids=[testServerID])
    async def remind(self, interaction: Interaction, message: Optional[str] = SlashOption(), time: Optional[str] = SlashOption()):
        def convert_time(time):
            pos = ["s", "m", "h", "d"]
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400}
            unit = time[-1]
            
            if unit not in pos:
                # Wrong / no unit given
                return -1
            
            try:
                val = int(time[:-1])
            except:
                # Time is not an integer
                return -2
            
            return val * time_dict[unit]
        converted_time = convert_time(time)
        
        # Misinput handeling
        if converted_time == -1:
            await interaction.response.send_message(f"Bitte eine andere Zeiteinheit (s, m, h, d) wählen!", ephemeral=True)
            
        elif converted_time == -2:
            await interaction.response.send_message(f"Die Zeit muss eine Zahl sein!", ephemeral=True)
        
        # Create reminder    
        else:       
            output = f"Reminder für `{message}` eingestellt! Ich erinnere dich in {time} daran."
            await interaction.send(f"{interaction.user.mention} {output}", ephemeral=True)
            await asyncio.sleep(converted_time)
            await interaction.send(f"{interaction.user.mention} Reminder: `{message}`", ephemeral=True)

# Add Cog to bot
def setup(bot):
    bot.add_cog(Basics(bot))
    print ("Basic functions loaded!")