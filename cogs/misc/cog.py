import nextcord
import asyncio
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from typing import Optional

# Initialize Cog
class Basics(commands.Cog, name="Misc"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Debug / Test-Command to see how well the bot is doing
    @nextcord.slash_command(name="ping", description="Pong!")
    async def ping(self, interaction: Interaction):
        await interaction.send(f"Pong! (`{round(self.bot.latency * 1000)}ms`)")
        
        
    # Custom help command
    @nextcord.slash_command(name="help", description="Verweist auf die Hilfe-Seite")
    async def help(self, interaction: Interaction):
        await interaction.response.send_message(f"Schau mal unter https://www.google.com/ nach!", ephemeral=True)
    
    
    # TODO: Add consistency check: Account for bot shutdown by saving reminders in DB
    # Reminder command (Supported: seconds, months, hours & days)
    @nextcord.slash_command(name="remindme", description="Lass dich an Dinge erinnern!")
    async def remind(self, interaction: Interaction, message: Optional[str] = SlashOption(), time: Optional[str] = SlashOption()):
        def convert_time(time):
            pos = ["s", "m", "h", "d", "sec", "min", "sek"]
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "sec": 1, "min": 60, "sek": 1}
            unit = time[-1]
            
            # Error handeling
            if unit not in pos:     # Wrong / no unit given
                return -1
            try:
                val = int(time[:-1])
            except:                 # Time is not an integer
                return -2
            
            return val * time_dict[unit]
        
        
        converted_time = convert_time(time)
        if converted_time == -1:    # Misinput handeling: Wrong unit
            await interaction.response.send_message(f"Bitte eine andere Zeiteinheit (s / sec / sek, m / min, h, d) wählen!", ephemeral=True)
        elif converted_time == -2:  # Misinput handeling: Integer Error
            await interaction.response.send_message(f"Die Zeit muss eine Zahl sein!", ephemeral=True)
        else:                       # Create reminder     
            output = f"Reminder für `{message}` eingestellt! Ich erinnere dich in {time} daran."
            await interaction.send(f"{interaction.user.mention} {output}", ephemeral=False)
            await asyncio.sleep(converted_time)
            await interaction.send(f"{interaction.user.mention} Reminder: `{message}`", ephemeral=False)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Basics(bot))
    print ("Basic functions loaded!")