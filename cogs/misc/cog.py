import nextcord
import asyncio
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from typing import Optional

# Initialize Cog
class Basics(commands.Cog, name="Misc"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # TODO: Add ping towards Stable Diffusion client
    # Debug / Test-Command to see how well the bot is doing
    @nextcord.slash_command(name="status", description="Pong!")
    async def status(self, interaction: Interaction):
        await interaction.send(f"Pong! (`{round(self.bot.latency * 1000)}ms`)")
    

    # Reminder command (Supported: seconds, months, hours & days)
    @nextcord.slash_command(name="remindme", description="Reminds you about things!")
    async def remind(self, interaction: Interaction, message: Optional[str] = SlashOption(), time: Optional[str] = SlashOption()):
        def convert_time(time):
            pos = ["s", "m", "h", "d", "sec", "min"]
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400, "sec": 1, "min": 60}
            unit = time[-1]
            
            # ! ERROR: Wrong / no unit given
            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            # ! ERROR: Time is not an integer
            except:                 
                return -2
            
            return val * time_dict[unit]
        
        
        converted_time = convert_time(time)
        # ! ERROR: wrong unit
        if converted_time == -1:    
            await interaction.response.send_message(f"Please use a different time unit `s / sec, m / min, h, d` !", ephemeral=True)
        # ! ERROR: Integer Error
        elif converted_time == -2:
            await interaction.response.send_message(f"Time needs to be a valid number!", ephemeral=True)
        # * Create reminder
        else:
            output = f"Reminder for `{message}` set! I'll remind you in `{time}`."
            await interaction.send(f"{interaction.user.mention} {output}", ephemeral=False)
            await asyncio.sleep(converted_time)
            await interaction.send(f"{interaction.user.mention} Reminder: `{message}`", ephemeral=False)


# Add Cog to bot
def setup(bot):
    bot.add_cog(Basics(bot))
    print ("Basic functions loaded!")